from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from database import get_db
from repository.book_repo import BookRepository
from schemas.book import BookCreate, BookResponse, BookStatus

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def get_books(
        limit: int = Query(10, ge=1, le=100, description="Кількість записів на сторінці"),
        offset: int = Query(0, ge=0, description="Скільки записів пропустити"),
        status_filter: Optional[BookStatus] = Query(None, alias="status"),
        author: Optional[str] = None,
        sort_by: Optional[str] = Query(None, description="Доступно: 'title' або 'year'"),
        db: AsyncSession = Depends(get_db)
):
    repo = BookRepository(db)
    status_val = status_filter.value if status_filter else None

    return await repo.get_all(
        limit=limit,
        offset=offset,
        status=status_val,
        author=author,
        sort_by=sort_by
    )


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