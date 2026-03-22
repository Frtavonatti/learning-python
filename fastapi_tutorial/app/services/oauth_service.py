from sqlalchemy.orm import Session
from app import models
from app.repositories.user_repository import UserRepository
from app.repositories.oauth_repository import OAuthRepository
from app.services.user_service import UserService


class OAuthUserService:
    """Service for OAuth authentication logic"""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.oauth_repo = OAuthRepository(db)
        self.user_service = UserService(db)

    def get_or_create_user(
        self,
        provider: str,
        provider_user_id: str,
        email: str,
        base_username: str,
    ) -> models.User:
        """
        Get or create a user from OAuth.
        
        Handles three cases:
        1. OAuth account exists → return linked user
        2. Email exists → link OAuth to existing user
        3. New user → create user and link OAuth
        
        Args:
            provider: OAuth provider name ('github', 'google')
            provider_user_id: User ID from the provider
            email: Verified user email
            base_username: Base username to generate a unique one
            
        Returns:
            User (existing or new) with OAuth linked
        """
        # 1. Look for existing OAuth account
        oauth_account = self.oauth_repo.get_by_provider_and_id(
            provider, provider_user_id
        )

        if oauth_account:
            # OAuth already linked, return user
            return oauth_account.user

        # 2. Look for user by email
        user = self.user_repo.get_by_email(email)

        if not user:
            # 3. Create new user
            user = self._create_oauth_user(email, base_username)

        # 4. Link OAuth to user (new or existing)
        self._link_oauth_account(user.id, provider, provider_user_id)

        return user

    def _create_oauth_user(self, email: str, base_username: str) -> models.User:
        """
        Create a new user from OAuth.
        
        Args:
            email: User email
            base_username: Base username to generate a unique one
            
        Returns:
            Created user (without commit)
        """
        username = self.user_service.generate_unique_username(base_username)

        user = models.User(
            email=email,
            username=username,
            hashed_password=None,  # OAuth doesn't require password
            roles=[],
        )

        return self.user_repo.create(user)

    def _link_oauth_account(
        self, user_id: int, provider: str, provider_user_id: str
    ) -> models.OAuthAccount:
        """
        Link an OAuth account to a user.
        
        Args:
            user_id: User ID
            provider: OAuth provider
            provider_user_id: User ID from the provider
            
        Returns:
            Created and committed OAuth account
        """
        oauth_account = models.OAuthAccount(
            user_id=user_id,
            provider=provider,
            provider_user_id=provider_user_id,
        )

        self.oauth_repo.create(oauth_account)
        self.oauth_repo.commit()

        return oauth_account
