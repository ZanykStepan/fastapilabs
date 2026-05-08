import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo_admin:password@mongo_db:27017/books?authSource=admin")
client = AsyncIOMotorClient(MONGO_URL)
db = client.books

async def get_db():
    yield db