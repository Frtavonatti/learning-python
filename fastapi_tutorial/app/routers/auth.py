from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from app import schemas, models
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login():
    pass


@router.post("/register")
async def register():
    pass
