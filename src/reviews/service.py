from .schemas import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from fastapi import status
import uuid
import logging


user_service = UserService()
book_service = BookService()


class ReviewService:
    async def add_book_review(
        self,
        book_uid: uuid.UUID,
        user_email: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        try:
            user = await user_service.get_user_by_email(user_email, session)
            book = await book_service.get_book(book_uid, session)

            if not book:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= "Book not found")

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not found")

            review_dict = review_data.model_dump()

            new_review = Review(**review_dict)

            new_review.user = user
            new_review.book = book

            session.add(new_review)
            await session.commit()

            return new_review
        
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Opps... Something went wrong"
            )
        