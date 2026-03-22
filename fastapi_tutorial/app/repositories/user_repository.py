from typing import Optional
from sqlalchemy.orm import Session
from app import models


class UserRepository:
    """Repository for user data access"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[models.User]:
        """Get user by ID"""
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[models.User]:
        """Get user by email"""
        return self.db.query(models.User).filter(models.User.email == email).first()

    def get_by_username(self, username: str) -> Optional[models.User]:
        """Get user by username"""
        return (
            self.db.query(models.User).filter(models.User.username == username).first()
        )

    def username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        return (
            self.db.query(models.User).filter(models.User.username == username).first()
            is not None
        )

    def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        return (
            self.db.query(models.User).filter(models.User.email == email).first()
            is not None
        )

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
