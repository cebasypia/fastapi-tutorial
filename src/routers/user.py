from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession

import src.cruds.user as user_crud
import src.schemas as schema
from src.db import get_db

router = APIRouter()


@router.get("/users", response_model=list[schema.User], status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_db)) -> list[schema.User]:
    return await user_crud.get_users(db)


@router.post("/users", response_model=schema.User, status_code=status.HTTP_201_CREATED)
async def create_user(user_body: schema.UserCreate, db: AsyncSession = Depends(get_db)) -> schema.User:
    return await user_crud.create_user(db, user_body)
