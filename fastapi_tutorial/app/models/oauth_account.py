from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class OAuthAccount(Base):
    """
    Stores OAuth provider linkages for users.
    A user can have multiple OAuth providers (GitHub, Google, etc.).
    """
    __tablename__ = "oauth_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider = Column(String, nullable=False)  # "github", "google", etc.
    provider_user_id = Column(String, nullable=False)  # OAuth provider's user ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="oauth_accounts")

    # Ensure one provider per user (can't link same GitHub account twice)
    __table_args__ = (
        UniqueConstraint("provider", "provider_user_id", name="unique_provider_account"),
        UniqueConstraint("user_id", "provider", name="unique_user_provider"),
    )
