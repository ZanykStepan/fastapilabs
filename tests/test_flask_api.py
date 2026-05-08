import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_books(client):
    res = client.get('/books')
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_create_book(client):
    new_book = {"title": "Test", "author": "Tester", "year": 2024}
    res = client.post('/books', json=new_book)
    assert res.status_code == 201
    assert res.get_json()['title'] == "Test"