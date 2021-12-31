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


@router.get("/users/{user_id}", response_model=schema.User, status_code=status.HTTP_200_OK)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)) -> schema.User:
    user: schema.User = await user_crud.get_user(db, schema.User(id=user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user

