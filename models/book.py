import uuid
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class BookModel(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="available")
    year = Column(Integer, nullable=False)