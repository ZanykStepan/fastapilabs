from fastapi import FastAPI
from api.endpoints import router as books_router

app = FastAPI(title="Бібліотека API", description="Лабораторна робота #4")

app.include_router(books_router)