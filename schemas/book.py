from pydantic import BaseModel
from typing import Optional, List

class BookBase(BaseModel):
    title: str
    author: str
    year: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: str
    class Config:
        from_attributes = True

class BookPaginationResponse(BaseModel):
    items: List[BookResponse]
    next_cursor: Optional[str]