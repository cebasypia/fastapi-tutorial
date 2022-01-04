from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ulid import ULID

import src.models as model
import src.schemas as schema


async def get_users(db: AsyncSession) -> list[model.User]:
    result = await db.execute(select(model.User).limit(20))
    return result.scalars().all()


async def create_user(db: AsyncSession, user_create: schema.UserCreate) -> model.User:
    user = model.User(id=str(ULID()), **user_create.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user: model.User) -> model.User:
    result = await db.execute(select(model.User).filter(model.User.id == user.id))
    users: list[model.User] = result.first()
    return users[0] if users is not None else None


async def update_user(db: AsyncSession, user_create: schema.UserCreate, user: model.User) -> model.User:
    user.name = user_create.name or user.name
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user: model.User) -> None:
    await db.delete(user)
    await db.commit()
