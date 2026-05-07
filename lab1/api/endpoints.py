from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from schemas.book import BookCreate, BookResponse, BookStatus
from services.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])
book_service = BookService()

@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def get_books(
    status_filter: Optional[BookStatus] = Query(None, alias="status"),
    author: Optional[str] = None,
    sort_by: Optional[str] = Query(None, description="Доступно: 'title' або 'year'")
):
    status_val = status_filter.value if status_filter else None
    return await book_service.get_all_books(status=status_val, author=author, sort_by=sort_by)

@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: UUID):
    book = await book_service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книгу не знайдено")
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    return await book_service.create_book(book)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    await book_service.delete_book(book_id)
    return None