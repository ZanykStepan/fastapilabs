import uuid
from sqlalchemy import Column, String, Integer
from database import Base

class BookModel(Base):
    __tablename__ = "books"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)