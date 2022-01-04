from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession

import src.cruds as crud
import src.schemas as schema
from src import firebase
from src.db import get_db

router = APIRouter()


@router.get("/users", response_model=list[schema.User], status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_db)) -> list[schema.User]:
    return await crud.get_users(db)


@router.post("/users", response_model=schema.User, status_code=status.HTTP_201_CREATED)
async def create_user(user_body: schema.UserCreate, db: AsyncSession = Depends(get_db)) -> schema.User:
    return await crud.create_user(db, user_body)


@router.get("/users/{user_id}", response_model=schema.User, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: str, is_authenticated: bool = Depends(firebase.is_authenticated), db: AsyncSession = Depends(get_db)
) -> schema.User:
    if is_authenticated is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )

    user: schema.User = await crud.get_user(db, schema.User(id=user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.put("/users/{user_id}", response_model=schema.User, status_code=status.HTTP_200_OK)
async def update_user(user_id: str, user_body: schema.UserCreate, db: AsyncSession = Depends(get_db)) -> schema.User:
    user: schema.User = await crud.get_user(db, schema.User(id=user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return await crud.update_user(db, user_body, user)


@router.delete("/users/{user_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)) -> None:
    user: schema.User = await crud.get_user(db, schema.User(id=user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return await crud.delete_user(db, user)
