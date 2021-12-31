from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ulid import ULID

from src.models.user import User
from src.schemas.user import UserCreate


async def get_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User).limit(20))
    return result.scalars().all()


async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    user = User(id=str(ULID()), **user_create.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user: User) -> User:
    result = await db.execute(select(User).filter(User.id == user.id))
    users: list[User] = result.first()
    return users[0] if users is not None else None


async def update_user(db: AsyncSession, user_create: UserCreate, user: User) -> User:
    user.name = user_create.name or user.name
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()
