from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid



class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(le=5, ge=1)
    review_text: str = Field(max_length=1000)
    user_uid: Optional[uuid.UUID] 
    book_uid: Optional[uuid.UUID]
    created_at: datetime

class ReviewCreateModel(BaseModel):
    rating: int = Field(le=5, ge=1)
    review_text: str = Field(max_length=1000)
