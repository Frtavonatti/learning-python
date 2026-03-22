from typing import Optional
from sqlalchemy.orm import Session
from app import models


class OAuthRepository:
    """Repository for OAuth account data access"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_provider_and_id(
        self, provider: str, provider_user_id: str
    ) -> Optional[models.OAuthAccount]:
        """Get OAuth account by provider and provider_user_id"""
        return (
            self.db.query(models.OAuthAccount)
            .filter_by(provider=provider, provider_user_id=provider_user_id)
            .first()
        )

    def create(self, oauth_account: models.OAuthAccount) -> models.OAuthAccount:
        """Create a new OAuth account"""
        self.db.add(oauth_account)
        self.db.flush()
        return oauth_account

    def commit(self):
        """Commit the transaction"""
        self.db.commit()
