from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime, date

from src.auth.schemas import UserModel
from src.reviews.schemas import ReviewModel

class BookSchema(BaseModel):
    uid: uuid.UUID
    user_uid: Optional[uuid.UUID]
    title: str
    author: str
    genre: str
    published_year: date
    language: str
    pagecount: int
    created_at: datetime
    updated_at: datetime

class BookDetailedSchema(BookSchema):
    user: Optional[UserModel] = None
    reviews: List[ReviewModel]



class BookCreateModel(BaseModel):
    title: str
    author: str
    genre: str
    published_year: date
    language: str
    pagecount: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    published_year: Optional[date] = None
    language: Optional[str] = None
    pagecount: Optional[int] = None