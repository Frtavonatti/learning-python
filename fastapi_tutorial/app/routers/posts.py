from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import schemas, models
from app.core.database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db)) -> list[models.Post]:
    posts = db.query(models.Post).all()
    return posts


@router.get("/{post_id}", response_model=schemas.PostOut)
async def get_post(post_id: int, db: Session = Depends(get_db)) -> models.Post:
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} was not found",
        )
    
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
async def create_post(
    post: schemas.PostCreate, db: Session = Depends(get_db)
) -> models.Post:
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    try:
        db.commit()
        db.refresh(new_post)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid owner_id or database constraint violation"
        )
    return new_post


@router.put("/{post_id}", response_model=schemas.PostOut)
async def update_post(
    post_id: int, post_update: schemas.PostUpdate, db: Session = Depends(get_db)
) -> models.Post:
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} was not found",
        )
    
    post_query.update(post_update.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)) -> Response:
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} was not found",
        )
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
