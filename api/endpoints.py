from fastapi import APIRouter, Depends, Query, status, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional

from database import get_db
from repository.book_repo import BookRepository
from schemas.book import BookCreate, BookResponse, BookStatus, BookPaginationResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=BookPaginationResponse, status_code=status.HTTP_200_OK)
async def get_books(
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        status_filter: Optional[BookStatus] = Query(None, alias="status"),
        author: Optional[str] = None,
        db: AsyncIOMotorDatabase = Depends(get_db)
):
    repo = BookRepository(db)
    status_val = status_filter.value if status_filter else None

    books = await repo.get_all(limit=limit, offset=offset, status=status_val, author=author)
    return {"items": books, "limit": limit, "offset": offset}


@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    repo = BookRepository(db)
    book = await repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книгу не знайдено")
    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    repo = BookRepository(db)
    return await repo.create(book.model_dump())


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    repo = BookRepository(db)
    await repo.delete(book_id)
    return None