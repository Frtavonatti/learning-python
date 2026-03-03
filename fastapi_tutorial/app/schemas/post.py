from pydantic import BaseModel


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
