from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from enum import Enum
from pydantic_mongo import ObjectIdField

class BookStatus(str, Enum):
    AVAILABLE = "available"
    ISSUED = "issued"

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    status: BookStatus = BookStatus.AVAILABLE
    year: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: ObjectIdField = Field(alias="_id")
    model_config = ConfigDict(populate_by_name=True)

class BookPaginationResponse(BaseModel):
    items: List[BookResponse]
    limit: int
    offset: int