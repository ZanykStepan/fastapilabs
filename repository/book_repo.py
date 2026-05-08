from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import Optional, List

class BookRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("books_collection")

    async def get_all(self, limit: int, offset: int, status: Optional[str] = None, author: Optional[str] = None) -> List[dict]:
        query = {}
        if status:
            query["status"] = status
        if author:
            query["author"] = author

        cursor = self.collection.find(query).skip(offset).limit(limit)
        books = await cursor.to_list(length=limit)
        return books

    async def get_by_id(self, book_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(book_id):
            return None
        return await self.collection.find_one({"_id": ObjectId(book_id)})

    async def create(self, book_data: dict) -> dict:
        result = await self.collection.insert_one(book_data)
        return await self.get_by_id(result.inserted_id)

    async def delete(self, book_id: str) -> bool:
        if not ObjectId.is_valid(book_id):
            return False
        response = await self.collection.delete_one({'_id': ObjectId(book_id)})
        return response.deleted_count > 0