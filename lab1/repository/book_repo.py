from typing import List, Dict, Optional
from uuid import UUID
from models.db import books_db


class BookRepository:
    async def get_all(self, status: Optional[str] = None, author: Optional[str] = None,
                      sort_by: Optional[str] = None) -> List[Dict]:
        result = books_db

        if status:
            result = [b for b in result if b["status"] == status]
        if author:
            result = [b for b in result if b["author"] == author]

        if sort_by == "title":
            result = sorted(result, key=lambda x: x["title"])
        elif sort_by == "year":
            result = sorted(result, key=lambda x: x["year"])

        return result

    async def get_by_id(self, book_id: UUID) -> Optional[Dict]:
        for book in books_db:
            if book["id"] == str(book_id):
                return book
        return None

    async def create(self, book_data: Dict) -> Dict:
        books_db.append(book_data)
        return book_data

    async def delete(self, book_id: UUID) -> None:
        for i, book in enumerate(books_db):
            if book["id"] == str(book_id):
                del books_db[i]
                break