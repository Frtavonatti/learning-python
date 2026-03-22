from typing import Optional
from sqlalchemy import exists, select
from sqlalchemy.orm import Session
from app import models


class UserRepository:
    """Repository for user data access"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[models.User]:
        """Get user by ID (uses identity map cache)"""
        return self.db.get(models.User, user_id)

    def get_by_email(self, email: str) -> Optional[models.User]:
        """Get user by email"""
        return self.db.query(models.User).filter_by(email=email).first()

    def get_by_username(self, username: str) -> Optional[models.User]:
        """Get user by username"""
        return self.db.query(models.User).filter_by(username=username).first()

    def username_exists(self, username: str) -> bool:
        """Check if username already exists (efficient EXISTS query)"""
        return self.db.query(exists().where(models.User.username == username)).scalar()

    def email_exists(self, email: str) -> bool:
        """Check if email already exists (efficient EXISTS query)"""
        return self.db.query(exists().where(models.User.email == email)).scalar()

    def create(self, user: models.User) -> models.User:
        """Create a new user"""
        self.db.add(user)
        self.db.flush()
        return user

    def commit(self):
        """Commit the transaction"""
        self.db.commit()

    def refresh(self, user: models.User):
        """Refresh user from DB"""
        self.db.refresh(user)
