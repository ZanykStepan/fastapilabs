from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from uuid import UUID

class BookStatus(str, Enum):
    AVAILABLE = "available"
    ISSUED = "issued"

class BookBase(BaseModel):
    title: str = Field(..., description="Назва книги")
    author: str = Field(..., description="Автор книги")
    description: Optional[str] = Field(None, description="Опис книги")
    status: BookStatus = Field(default=BookStatus.AVAILABLE, description="Статус книги")
    year: int = Field(..., description="Рік випуску")

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: UUID