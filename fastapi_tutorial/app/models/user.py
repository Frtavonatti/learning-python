from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True) # nullable to allow OAuth strategy
    roles = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # OAuth fields
    oauth_providers = Column(String, nullable=True)
    oauth_provider_id = Column(String, nullable=True)

    # Relationships
    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="owner", cascade="all, delete-orphan"
    )
