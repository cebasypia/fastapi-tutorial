from sqlalchemy.ext.asyncio import AsyncSession
from ulid import ULID

from src.models import User


async def seed(async_session: AsyncSession):
    users: list[User] = []
    users.append(User(id="12345678901234567890123456", name="誠"))
    users.append(User(id=str(ULID()), name="稀"))
    users.append(User(id=str(ULID()), name="アビ"))

    async with async_session() as session:
        session.add_all(users)
        await session.commit()


if __name__ == "__main__":
    BOS = "\033[92m"  # 緑色表示用
    EOS = "\033[0m"

    print(f"{BOS}Seeding data...{EOS}")
    seed()
