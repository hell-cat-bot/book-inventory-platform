from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
import uuid

from src.auth.dependencies import get_current_user
from src.db.main import get_session
from src.db.models import User
from .service import ReviewService
from src.books.service import BookService
from .schemas import ReviewCreateModel, ReviewModel
from src.auth.dependencies import RoleChecker

review_router = APIRouter()

review_service = ReviewService()
book_service = BookService()
role_checker = RoleChecker(['admin','user'])


@review_router.post('/book/{book_uid}')
async def add_review_to_book(
    book_uid: uuid.UUID,
    review_data: ReviewCreateModel,
    user_data: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    review_data = await review_service.add_book_review(
        book_uid=book_uid, 
        user_email= user_data.email, 
        review_data=review_data, 
        session=session
    )

    return review_data

# Public endpoint
@review_router.get('/{review_uid}', response_model=ReviewModel)
async def get_review_by_uid(
    review_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    review = await review_service.get_review(review_uid=review_uid, session=session)

    if not review:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    return review


@review_router.get('/book/{book_uid}', response_model=List[ReviewModel])
async def get_all_reviews_of_book(
    book_uid: uuid.UUID,
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session)
):
    book = await book_service.get_book(
        book_uid = book_uid, 
        session = session
    )

    if not book:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Book not found'
        )
    
    reviews = await review_service.get_all_reviews(
        book_uid = book_uid,
        skip = skip,
        limit = limit,
        session = session
    )
    
    return reviews


@review_router.delete('/{review_uid}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_uid: uuid.UUID,
    user: User = Depends(role_checker),
    session: AsyncSession = Depends(get_session)
):
    await review_service.delete_review_from_book(
        review_uid = review_uid,
        user = user,
        session = session
    )

    return None