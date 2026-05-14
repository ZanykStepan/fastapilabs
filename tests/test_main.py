import httpx
import pytest

PRISM_URL = "http://localhost:4010"
HEADERS = {
    "Authorization": "Bearer fake-test-token"
}


@pytest.mark.asyncio
async def test_prism_get_books():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRISM_URL}/books/", headers=HEADERS)

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert "items" in data
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_prism_unauthorized_access():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRISM_URL}/books/")

    assert response.status_code == 401
