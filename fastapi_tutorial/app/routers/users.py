from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)) -> list[models.User]:
    users = db.query(models.User).all()
    return users


@router.get("/{user_id}", response_model=schemas.UserOut)
async def get_user(user_id: int, db: Session = Depends(get_db)) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} was not found",
        )

    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> models.User:
    # Check if email already exists
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Check if username already exists
    existing_username = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # TODO: Hash password before saving (usar passlib o bcrypt)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{user_id}", response_model=schemas.UserOut)
async def update_user(
    user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)
) -> models.User:
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} was not found",
        )

    # Filter out None values to only update provided fields
    update_data = user_update.model_dump(exclude_unset=True)

    # Check email uniqueness if being updated
    if "email" in update_data:
        existing_user = (
            db.query(models.User)
            .filter(
                models.User.email == update_data["email"], models.User.id != user_id
            )
            .first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    # Check username uniqueness if being updated
    if "username" in update_data:
        existing_username = (
            db.query(models.User)
            .filter(
                models.User.username == update_data["username"],
                models.User.id != user_id,
            )
            .first()
        )
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

    user_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> Response:
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} was not found",
        )

    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
