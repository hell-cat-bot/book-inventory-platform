from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid

from src.auth.dependencies import get_current_user
from src.db.main import get_session
from src.db.models import User
from .service import ReviewService
from .schemas import ReviewCreateModel

review_router = APIRouter()

review_service = ReviewService()


@review_router.post('/book/{book_uid}')
async def add_review_to_book(
    book_uid: uuid.UUID,
    review_data: ReviewCreateModel,
    user_data: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    review_data = review_service.add_book_review(
        book_uid=book_uid, 
        user_email= user_data.email, 
        review_data=review_data, 
        session=session
    )

    return review_data

