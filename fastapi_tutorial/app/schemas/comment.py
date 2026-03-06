from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CommentBase(BaseModel):
    text: str
    upvotes: int = 0
    downvotes: int = 0


class CommentCreate(CommentBase):
    owner_id: int
    post_id: int


class CommentUpdate(BaseModel):
    text: str | None = None
    upvotes: int | None = None
    downvotes: int | None = None


class CommentOut(CommentBase):
    id: int
    owner_id: int
    post_id: int
    created_at: datetime
    updated_at: datetime | None = None
    
    model_config = ConfigDict(from_attributes=True)
