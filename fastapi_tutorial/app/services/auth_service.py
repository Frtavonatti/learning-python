from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError

from app import models, schemas
from app.core.security import hash_password, verify_password
from app.auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


class AuthService:
    """Service for authentication logic (login, register, tokens)"""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.user_service = UserService(db)

    def register_user(self, user_data: schemas.UserCreate) -> models.User:
        """
        Register a new user with email/password.
        
        Args:
            user_data: User data to create
            
        Returns:
            Created user
            
        Raises:
            HTTPException: If email or username already exists
        """
        # Validate unique email
        if self.user_service.email_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Validate unique username
        if self.user_service.username_exists(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

        # Create user
        user_dict = user_data.model_dump()
        user_dict["hashed_password"] = hash_password(user_dict.pop("password"))

        new_user = models.User(**user_dict)
        self.user_repo.create(new_user)
        self.user_repo.commit()
        self.user_repo.refresh(new_user)

        return new_user

    def authenticate_user(self, email: str, password: str) -> models.User:
        """
        Authenticate a user with email/password.
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            Authenticated user
            
        Raises:
            HTTPException: If user doesn't exist or password is incorrect
        """
        user = self.user_repo.get_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This account uses OAuth. Please login with your OAuth provider.",
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        return user

    def create_tokens(self, user: models.User) -> schemas.Token:
        """
        Generate access and refresh tokens for a user.
        
        Args:
            user: Authenticated user
            
        Returns:
            Token response with access_token and refresh_token
        """
        access_token = create_access_token(subject=str(user.id), roles=user.roles)
        refresh_token = create_refresh_token(subject=str(user.id))

        return schemas.Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    def refresh_tokens(self, refresh_token: str) -> schemas.Token:
        """
        Generate new tokens from a refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New access and refresh tokens
            
        Raises:
            HTTPException: If token is invalid or user doesn't exist
        """
        try:
            payload = decode_token(refresh_token)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        if payload.get("token_type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type: expected refresh token",
            )

        user = self.user_repo.get_by_id(int(payload["sub"]))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return self.create_tokens(user)
