from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime, date

from src.auth.models import User

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
    user: Optional[User] = None


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