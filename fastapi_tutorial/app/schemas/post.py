from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PostBase(BaseModel):
	title: str
	content: str
	published: bool = True
	rating: int | None = None


class PostCreate(PostBase):
	pass


class PostUpdate(PostBase):
	pass


class PostOut(PostBase):
	id: int
	created_at: datetime | None = None
	updated_at: datetime | None = None
	
	model_config = ConfigDict(from_attributes=True)
