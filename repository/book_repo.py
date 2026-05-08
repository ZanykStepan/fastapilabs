from sqlalchemy import select, delete, asc
from sqlalchemy.ext.asyncio import AsyncSession
from models.book import BookModel
from uuid import UUID
from typing import List, Optional, Any, Dict

class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_cursor(
            self,
            limit: int,
            cursor: Optional[UUID] = None,
            status: Optional[str] = None,
            author: Optional[str] = None
    ) -> List[BookModel]:
        # Важливо: Cursor pagination потребує стабільного сортування (зазвичай по ID)
        query = select(BookModel).order_by(asc(BookModel.id)).limit(limit)

        # Якщо курсор передано, беремо записи, ID яких "більші" за курсор
        if cursor:
            query = query.where(BookModel.id > cursor)

        if status:
            query = query.where(BookModel.status == status)
        if author:
            query = query.where(BookModel.author == author)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, book_data: dict):
        new_book = BookModel(**book_data)
        self.db.add(new_book)
        await self.db.commit()
        await self.db.refresh(new_book)
        return new_book

    async def get_by_id(self, book_id: UUID):
        result = await self.db.execute(select(BookModel).where(BookModel.id == book_id))
        return result.scalar_one_or_none()

    async def delete(self, book_id: UUID):
        await self.db.execute(delete(BookModel).where(BookModel.id == book_id))
        await self.db.commit()