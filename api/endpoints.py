from fastapi import APIRouter, Depends, Request, Query, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from rate_limiter import rate_limit
from database import get_db
from repository.book_repo import BookRepository
from schemas.book import (
    BookCreate,
    BookResponse,
    BookStatus,
    BookPaginationResponse
)
from security import (
    verify_password,
    create_access_token,
    create_refresh_token
)

router = APIRouter(tags=["Books"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


@router.post("/login")
async def login(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    await rate_limit(request, user_id=None)

    if form_data.username != "admin" or form_data.password != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(data={"sub": form_data.username})
    refresh_token = create_refresh_token(data={"sub": form_data.username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
async def refresh_token(request: Request, refresh_token: str):
    await rate_limit(request, user_id=None)

    new_access_token = create_access_token(data={"sub": "admin"})
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.get(
    "/books/",
    response_model=BookPaginationResponse
)
async def get_books(
        request: Request,
        limit: int = Query(10, ge=1, le=100),
        cursor: Optional[UUID] = Query(None, description="ID останньої книги з попередньої сторінки"),
        status_filter: Optional[BookStatus] = None,
        author: Optional[str] = None,
        token: Optional[str] = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    user_id = "admin" if token else None
    await rate_limit(request, user_id=user_id)

    repo = BookRepository(db)
    books = await repo.get_all_cursor(
        limit=limit,
        cursor=cursor,
        status=status_filter.value if status_filter else None,
        author=author
    )

    next_cursor = books[-1].id if len(books) == limit else None

    return {
        "items": books,
        "next_cursor": next_cursor
    }


@router.get(
    "/books/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK
)
async def get_book(
        request: Request,
        book_id: UUID,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    await rate_limit(request, user_id="admin")

    repo = BookRepository(db)
    book = await repo.get_by_id(book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книгу не знайдено"
        )

    return book


@router.post(
    "/books/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_book(
        request: Request,
        book: BookCreate,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    await rate_limit(request, user_id="admin")

    repo = BookRepository(db)
    return await repo.create(book.model_dump())


@router.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(
        request: Request,
        book_id: UUID,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    await rate_limit(request, user_id="admin")

    repo = BookRepository(db)
    await repo.delete(book_id)
    return None