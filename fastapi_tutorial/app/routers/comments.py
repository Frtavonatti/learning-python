from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.database import get_db

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=list[schemas.CommentOut])
async def get_comments(db: Session = Depends(get_db)) -> list[models.Comment]:
    """Get all comments."""
    comments = db.query(models.Comment).all()
    return comments


@router.get("/post/{post_id}", response_model=list[schemas.CommentOut])
async def get_comments_by_post(
    post_id: int, db: Session = Depends(get_db)
) -> list[models.Comment]:
    """Get all comments for a specific post."""
    # Check if post exists
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} was not found",
        )
    
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    return comments


@router.get("/{comment_id}", response_model=schemas.CommentOut)
async def get_comment(
    comment_id: int, db: Session = Depends(get_db)
) -> models.Comment:
    """Get a single comment by ID."""
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} was not found",
        )
    
    return comment


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentOut)
async def create_comment(
    comment: schemas.CommentCreate, db: Session = Depends(get_db)
) -> models.Comment:
    """Create a new comment."""
    # Verify that user exists
    user = db.query(models.User).filter(models.User.id == comment.owner_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {comment.owner_id} was not found",
        )
    
    # Verify that post exists
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {comment.post_id} was not found",
        )
    
    new_comment = models.Comment(**comment.model_dump())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.put("/{comment_id}", response_model=schemas.CommentOut)
async def update_comment(
    comment_id: int, comment_update: schemas.CommentUpdate, db: Session = Depends(get_db)
) -> models.Comment:
    """Update a comment."""
    comment_query = db.query(models.Comment).filter(models.Comment.id == comment_id)
    comment = comment_query.first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} was not found",
        )
    
    # Only update fields that were provided
    update_data = comment_update.model_dump(exclude_unset=True)
    comment_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int, db: Session = Depends(get_db)
) -> Response:
    """Delete a comment."""
    comment_query = db.query(models.Comment).filter(models.Comment.id == comment_id)
    comment = comment_query.first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} was not found",
        )
    
    comment_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
