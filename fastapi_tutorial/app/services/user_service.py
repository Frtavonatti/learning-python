from sqlalchemy.orm import Session
from app import models
from app.repositories.user_repository import UserRepository


class UserService:
    """Service for user business logic"""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def generate_unique_username(self, base: str) -> str:
        """
        Generate a unique username by adding numeric suffixes if necessary.
        
        Args:
            base: Base username (e.g., "john", "github_12345")
            
        Returns:
            Unique username (e.g., "john", "john_1", "john_2")
        """
        username = base
        suffix = 1
        while self.user_repo.username_exists(username):
            username = f"{base}_{suffix}"
            suffix += 1
        return username

    def get_by_id(self, user_id: int) -> models.User | None:
        """Get user by ID"""
        return self.user_repo.get_by_id(user_id)

    def get_by_email(self, email: str) -> models.User | None:
        """Get user by email"""
        return self.user_repo.get_by_email(email)

    def email_exists(self, email: str) -> bool:
        """Check if email is already registered"""
        return self.user_repo.email_exists(email)

    def username_exists(self, username: str) -> bool:
        """Check if username is already taken"""
        return self.user_repo.username_exists(username)
