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
async def test_create_book(async_client: AsyncClient):
    response = await async_client.post("/books/", json={
        "title": "Clean Architecture",
        "author": "Robert C. Martin",
        "description": "Software Structure and Design",
        "status": "available",
        "year": 2017
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Clean Architecture"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_books_filtered_and_sorted(async_client: AsyncClient):
    await async_client.post("/books/",
                            json={"title": "B Book", "author": "Author A", "status": "available", "year": 2022})
    await async_client.post("/books/",
                            json={"title": "A Book", "author": "Author A", "status": "available", "year": 2020})
    await async_client.post("/books/", json={"title": "C Book", "author": "Author B", "status": "issued", "year": 2021})

    res_author = await async_client.get("/books/?author=Author A")
    assert res_author.status_code == 200
    assert len(res_author.json()) == 2

    res_sort = await async_client.get("/books/?sort_by=year")
    assert res_sort.status_code == 200
    assert res_sort.json()[0]["title"] == "A Book"


@pytest.mark.asyncio
async def test_get_book_not_found(async_client: AsyncClient):
    response = await async_client.get("/books/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_book_idempotent(async_client: AsyncClient):
    create_res = await async_client.post("/books/", json={
        "title": "To Delete", "author": "Anon", "status": "available", "year": 2000
    })
    book_id = create_res.json()["id"]

    del_res1 = await async_client.delete(f"/books/{book_id}")
    assert del_res1.status_code == 204

    del_res2 = await async_client.delete(f"/books/{book_id}")
    assert del_res2.status_code == 204