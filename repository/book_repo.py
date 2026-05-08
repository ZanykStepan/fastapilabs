from sqlalchemy.future import select
from models.book import BookModel

class BookRepository:
    def __init__(self, db):
        self.db = db

    async def get_all(self, limit: int, offset: int):
        result = await self.db.execute(select(BookModel).offset(offset).limit(limit))
        return result.scalars().all()

    async def create(self, book_data: dict):
        new_book = BookModel(**book_data)
        self.db.add(new_book)
        await self.db.commit()
        await self.db.refresh(new_book)
        return new_book