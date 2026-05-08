from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.book import BookModel
from uuid import UUID
from typing import Optional


class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, limit: int, offset: int, status: Optional[str] = None, author: Optional[str] = None,
                      sort_by: Optional[str] = None):
        query = select(BookModel).limit(limit).offset(offset)

        if status:
            query = query.where(BookModel.status == status)
        if author:
            query = query.where(BookModel.author == author)

        if sort_by == "title":
            query = query.order_by(BookModel.title)
        elif sort_by == "year":
            query = query.order_by(BookModel.year)

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