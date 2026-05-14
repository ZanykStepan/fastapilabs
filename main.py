from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.endpoints import router as books_router
from database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Бібліотека API", description="Лабораторна робота #8", lifespan=lifespan)

app.include_router(books_router)