from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.database import get_db
from app.core.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    
    # TODO: Generate JWT token here
    return {"message": "Login successful", "user_id": existing_user.id}


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,  # Filters response - only returns UserOut fields (without hashed_password)
)
async def register(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> models.User:
    # Check if email already exists
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Check if username already exists
    existing_username = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    user_data = user.model_dump()
    user_data["hashed_password"] = hash_password(user_data.pop("password"))

    # ** unpacks dictionary into kwargs: User(email="...", username="...", hashed_password="...")
    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user  # Returns full User, but FastAPI filters using UserOut
