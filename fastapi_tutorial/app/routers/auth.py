from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.core.database import get_db
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.Token)
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    authenticated_user = auth_service.authenticate_user(user.email, user.password)
    return auth_service.create_tokens(authenticated_user)



@router.post("/refresh", response_model=schemas.Token)
async def refresh(body: schemas.RefreshTokenRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.refresh_tokens(body.refresh_token)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    new_user = auth_service.register_user(user)
    return new_user
