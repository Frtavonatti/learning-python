# DEPRECATED: Use app.services.user_service, app.services.auth_service, app.services.oauth_service
# This file is kept for backwards compatibility

from sqlalchemy.orm import Session
from app import models

# Import new services for backwards compatibility
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.oauth_service import OAuthUserService


def get_user_by_id(db: Session, id: str):
    """DEPRECATED: Use UserService.get_by_id() instead"""
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


def get_user_by_email(db: Session, email: str):
    """DEPRECATED: Use UserService.get_by_email() instead"""
    user = db.query(models.User).filter(models.User.email == email).first()
    return user
