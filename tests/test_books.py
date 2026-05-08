import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from database import engine, Base
from schemas.book import BookPaginationResponse
from typing import List, Optional


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
async def test_cursor_pagination(async_client: AsyncClient):
    for i in range(5):
        await async_client.post("/books/", json={
            "title": f"Book {i}",
            "author": "Tester",
            "description": "Desc",
            "status": "available",
            "year": 2000 + i
        })

    res1 = await async_client.get("/books/?limit=2")
    assert res1.status_code == 200
    data1 = res1.json()

    assert len(data1["items"]) == 2
    cursor = data1["next_cursor"]
    assert cursor is not None

    res2 = await async_client.get(f"/books/?limit=2&cursor={cursor}")
    assert res2.status_code == 200
    data2 = res2.json()

    assert len(data2["items"]) == 2
    assert data2["items"][0]["id"] != data1["items"][0]["id"]