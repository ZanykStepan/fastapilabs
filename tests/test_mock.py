import requests

def test_mock_get_books():
    response = requests.get("http://127.0.0.1:4010/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]['title'] == "Clean Code"

def test_mock_validation_error():
    response = requests.post(
        "http://127.0.0.1:4010/books",
        json={"title": "Test", "author": "Tester", "year": "not-a-number"}
    )
    assert response.status_code >= 400