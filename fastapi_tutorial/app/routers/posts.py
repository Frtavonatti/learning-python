from fastapi import APIRouter, HTTPException, Response, status

from app import schemas

router = APIRouter(prefix="/posts", tags=["Posts"])

mock_posts: list[dict] = [
    {
        "id": 1,
        "title": "Primer post",
        "content": "Bienvenido al tutorial de FastAPI para blog.",
        "published": True,
        "rating": 5,
    },
    {
        "id": 2,
        "title": "Segundo post",
        "content": "Este es otro blogpost usando mockdata.",
        "published": True,
        "rating": 4,
    },
]


@router.get("/", response_model=list[schemas.PostOut])
async def get_posts() -> list[dict]:
    return mock_posts


@router.get("/{post_id}", response_model=schemas.PostOut)
async def get_post(post_id: int) -> dict:
    for post in mock_posts:
        if post["id"] == post_id:
            return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {post_id} was not found",
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
async def create_post(post: schemas.PostCreate) -> dict:
    next_id = max((item["id"] for item in mock_posts), default=0) + 1
    new_post = {"id": next_id, **post.model_dump()}
    mock_posts.append(new_post)
    return new_post


@router.put("/{post_id}", response_model=schemas.PostOut)
async def update_post(post_id: int, post: schemas.PostUpdate) -> dict:
    for index, existing_post in enumerate(mock_posts):
        if existing_post["id"] == post_id:
            updated_post = {"id": post_id, **post.model_dump()}
            mock_posts[index] = updated_post
            return updated_post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {post_id} was not found",
    )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int) -> Response:
    for index, post in enumerate(mock_posts):
        if post["id"] == post_id:
            del mock_posts[index]
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {post_id} was not found",
    )
