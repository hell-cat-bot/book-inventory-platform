from .schemas import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi.exceptions import HTTPException
from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from fastapi import status
from typing import List
import uuid
import logging


user_service = UserService()
book_service = BookService()


class ReviewService:
    # Add Review
    async def add_book_review(
        self,
        book_uid: uuid.UUID,
        user_email: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ) -> Review:

        try:
            user = await user_service.get_user_by_email(user_email, session)
            book = await book_service.get_book(book_uid, session)

            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
                )

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )

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
                detail="Opps... Something went wrong",
            )

    # Get Review
    async def get_review(self, review_uid: uuid.UUID, session: AsyncSession) -> Review:
        statement = select(Review).where(Review.uid == review_uid)

        review_data = await session.exec(statement)

        return review_data.first()

    # Get all review of a book - by paagination
    async def get_all_reviews(
        self, book_uid: uuid.UUID, skip: int, limit: int, session: AsyncSession
    ) -> List[Review]:
        statement = (
            select(Review).where(Review.book_uid == book_uid).offset(skip).limit(limit)
        )

        reviews = await session.exec(statement)

        # returns a [] if no reviews exist , dont raise -404- its Anti-Practice
        return reviews.all()

    # Delete review
    async def delete_review_from_book(
        self, review_uid: uuid.UUID, user: User, session: AsyncSession
    ) -> None:
        review = await self.get_review(review_uid=review_uid, session=session)

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
            )

        # Only "admin" and 'user' who made the review are allowed to delete
        if review.user_uid != user.uid and user.role != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this comment",
            )

        await session.delete(review)

        await session.commit()

        return None
