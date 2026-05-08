from typing import List, Optional
from uuid import UUID, uuid4
from schemas.book import BookCreate, BookResponse
from repository.book_repo import BookRepository


class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def get_all_books(self, status: Optional[str] = None, author: Optional[str] = None,
                            sort_by: Optional[str] = None) -> List[BookResponse]:
        books_data = await self.repo.get_all(status, author, sort_by)
        return [BookResponse(**book) for book in books_data]

    async def get_book_by_id(self, book_id: UUID) -> Optional[BookResponse]:
        book_data = await self.repo.get_by_id(book_id)
        if book_data:
            return BookResponse(**book_data)
        return None

    async def create_book(self, book_in: BookCreate) -> BookResponse:
        new_book_id = uuid4()
        book_dict = book_in.model_dump()
        book_dict["id"] = str(new_book_id)
        book_dict["status"] = book_dict["status"].value

        created_book = await self.repo.create(book_dict)
        return BookResponse(**created_book)

    async def delete_book(self, book_id: UUID) -> None:
        await self.repo.delete(book_id)