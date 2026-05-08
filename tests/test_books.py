import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from database import engine, Base


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_get_books_unauthorized(async_client: AsyncClient):
    response = await async_client.get("/books/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_and_access(async_client: AsyncClient):
    login_res = await async_client.post("/login", data={
        "username": "admin",
        "password": "admin"
    })
    assert login_res.status_code == 200

    token_data = login_res.json()
    assert "access_token" in token_data
    access_token = token_data["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.get("/books/", headers=headers)

    assert response.status_code == 200
    assert "items" in response.json()


@pytest.mark.asyncio
async def test_refresh_token_simple(async_client: AsyncClient):
    response = await async_client.post("/refresh", params={"refresh_token": "some_token"})
    assert response.status_code == 200
    assert "access_token" in response.json()