from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


async def get_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User).limit(20))
    return result.scalars().all()
