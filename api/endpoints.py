from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from repository.book_repo import BookRepository
from schemas.book import BookCreate, BookResponse, BookPaginationResponse
from security import create_access_token

router = APIRouter(tags=["Books"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "admin" and form_data.password == "admin":
        return {"access_token": create_access_token({"sub": "admin"}), "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect login")

@router.get("/books/", response_model=BookPaginationResponse)
async def get_books(db: AsyncSession = Depends(get_db)):
    repo = BookRepository(db)
    books = await repo.get_all(limit=10, offset=0)
    return {"items": books, "next_cursor": None}

@router.post("/books/", response_model=BookResponse)
async def create_book(book: BookCreate, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    repo = BookRepository(db)
    return await repo.create(book.model_dump())