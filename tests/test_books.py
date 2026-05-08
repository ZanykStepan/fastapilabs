import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from database import db

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    await db.books_collection.delete_many({})
    yield

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_book(async_client: AsyncClient):
    response = await async_client.post("/books/", json={
        "title": "Mongo Book",
        "author": "Tester",
        "year": 2024,
        "status": "available"
    })
    assert response.status_code == 201
    data = response.json()
    assert "_id" in data