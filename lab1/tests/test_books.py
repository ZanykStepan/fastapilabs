import pytest
from fastapi.testclient import TestClient
from main import app
from models.db import books_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    books_db.clear()


def test_create_book():
    response = client.post("/books/", json={
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


def test_get_books_filtered_and_sorted():
    client.post("/books/", json={"title": "B Book", "author": "Author A", "status": "available", "year": 2022})
    client.post("/books/", json={"title": "A Book", "author": "Author A", "status": "available", "year": 2020})
    client.post("/books/", json={"title": "C Book", "author": "Author B", "status": "issued", "year": 2021})

    res_author = client.get("/books/?author=Author A")
    assert res_author.status_code == 200
    assert len(res_author.json()) == 2

    res_sort = client.get("/books/?sort_by=year")
    assert res_sort.status_code == 200
    assert res_sort.json()[0]["title"] == "A Book"


def test_get_book_not_found():
    response = client.get("/books/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 404


def test_delete_book_idempotent():
    create_res = client.post("/books/", json={
        "title": "To Delete", "author": "Anon", "status": "available", "year": 2000
    })
    book_id = create_res.json()["id"]

    del_res1 = client.delete(f"/books/{book_id}")
    assert del_res1.status_code == 204

    del_res2 = client.delete(f"/books/{book_id}")
    assert del_res2.status_code == 204

    get_res = client.get(f"/books/{book_id}")
    assert get_res.status_code == 404