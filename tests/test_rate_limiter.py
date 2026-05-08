import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from rate_limiter import rate_limit

app = FastAPI()

@app.get("/test-anon")
async def anon_handler(request: Request):
    await rate_limit(request, user_id=None)
    return {"status": "ok"}

@app.get("/test-auth")
async def auth_handler(request: Request):
    await rate_limit(request, user_id="test_user")
    return {"status": "ok"}

client = TestClient(app)

@pytest.mark.asyncio
async def test_anon():
    pass

@pytest.mark.asyncio
async def test_auth():
    pass


@patch("rate_limiter.redis_db.pipeline")
def test_anonymous_under_limit(mock_pipeline):
    mock_pipe = MagicMock()
    mock_pipe.execute = AsyncMock(return_value=[0, 1, 0, True])
    mock_pipeline.return_value.__aenter__.return_value = mock_pipe

    response = client.get("/test-anon")
    assert response.status_code == 200

@patch("rate_limiter.redis_db.pipeline")
def test_anonymous_over_limit(mock_pipeline):
    mock_pipe = MagicMock()
    mock_pipe.execute = AsyncMock(return_value=[0, 2, 0, True])
    mock_pipeline.return_value.__aenter__.return_value = mock_pipe

    response = client.get("/test-anon")
    assert response.status_code == 429

@patch("rate_limiter.redis_db.pipeline")
def test_authenticated_under_limit(mock_pipeline):
    mock_pipe = MagicMock()
    mock_pipe.execute = AsyncMock(return_value=[0, 9, 0, True])
    mock_pipeline.return_value.__aenter__.return_value = mock_pipe

    response = client.get("/test-auth")
    assert response.status_code == 200

@patch("rate_limiter.redis_db.pipeline")
def test_authenticated_over_limit(mock_pipeline):
    mock_pipe = MagicMock()
    mock_pipe.execute = AsyncMock(return_value=[0, 10, 0, True])
    mock_pipeline.return_value.__aenter__.return_value = mock_pipe

    response = client.get("/test-auth")
    assert response.status_code == 429