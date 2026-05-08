from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from database import get_db
from repository.book_repo import BookRepository
from schemas.book import BookCreate, BookResponse, BookStatus, BookPaginationResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=BookPaginationResponse)
async def get_books(
        limit: int = Query(10, ge=1, le=100),
        cursor: Optional[UUID] = Query(None, description="ID останньої книги з попередньої сторінки"),
        status: Optional[BookStatus] = None,
        author: Optional[str] = None,
        db: AsyncSession = Depends(get_db)
):
    repo = BookRepository(db)
    books = await repo.get_all_cursor(
        limit=limit,
        cursor=cursor,
        status=status.value if status else None,
        author=author
    )

    next_cursor = books[-1].id if len(books) == limit else None

    return {
        "items": books,
        "next_cursor": next_cursor
    }

@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BookRepository(db)
    book = await repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книгу не знайдено")
    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    repo = BookRepository(db)
    return await repo.create(book.model_dump())


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BookRepository(db)
    await repo.delete(book_id)
    return None