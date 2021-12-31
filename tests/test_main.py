import pytest
import starlette.status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.db import Base, get_db
from src.main import app
from tests.seed import seed

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def async_client() -> AsyncClient:
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

    # テスト用にオンメモリのSQLiteテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    await seed(async_session)

    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_get_users(async_client):
    response = await async_client.get("/users")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 3
    assert response_obj[0]["name"] == "誠"
    assert len(response_obj[0]["id"]) == 26


@pytest.mark.asyncio
async def test_create_user(async_client):
    response = await async_client.post("/users", json={"name": "テストユーザー"})
    assert response.status_code == starlette.status.HTTP_201_CREATED
    response_obj = response.json()
    assert response_obj["name"] == "テストユーザー"


@pytest.mark.asyncio
async def test_get_user(async_client):
    response = await async_client.get("/users/12345678901234567890123456")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["name"] == "誠"


@pytest.mark.asyncio
async def test_update_user(async_client):
    response = await async_client.put("/users/12345678901234567890123456", json={"name": "まこと"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["name"] == "まこと"


@pytest.mark.asyncio
async def test_delete_user(async_client):
    response = await async_client.delete("/users/12345678901234567890123456")
    assert response.status_code == starlette.status.HTTP_204_NO_CONTENT
    response_obj = response.json()
    assert response_obj is None
