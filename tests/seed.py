# seed.py

# from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# from src.db import get_db
from src.models import User

# from sqlalchemy.orm import sessionmaker


async def seed(async_session: AsyncSession):
    users: list[User] = []
    users.append(User(id="12345678901234567890123456", name="誠"))
    users.append(User(id="22345678901234567890123456", name="稀"))
    users.append(User(id="32345678901234567890123456", name="アビ"))

    async with async_session() as session:
        session.add_all(users)
        await session.commit()


if __name__ == "__main__":
    BOS = "\033[92m"  # 緑色表示用
    EOS = "\033[0m"

    print(f"{BOS}Seeding data...{EOS}")
    seed()
