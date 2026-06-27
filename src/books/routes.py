from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status, Depends
from typing import List
import uuid


from src.books.schemas import BookSchema, BookUpdate, BookCreateModel,BookDetailedSchema
from src.db.main import get_session
from src.db.models import User
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer, RoleChecker




api_router = APIRouter()

book_service = BookService()


role_checker = RoleChecker(["admin", "user"])





@api_router.get("/", response_model=List[BookSchema])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(role_checker),  # Credential
):

    books = await book_service.get_all_books(session)
    return books



@api_router.get("/user/{user_uid}", response_model=List[BookSchema])
async def get_user_book_submissions(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(role_checker)
):
    books = await book_service.get_user_books(user_uid, session)
    
    return books




@api_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=BookSchema
)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(role_checker),
):
    user_uid = user.uid
    new_book = await book_service.create_book(book_data,user_uid, session)
    return new_book


"""
if we keep our "book_uid: str" as a string then if the user gives some garbage like 'asddgreg322' it will crash the server without proper handling
so using "book_uid: uuid.UUID" is better as if any garbage comes FastAPI throws a 407
"""


@api_router.get("/{book_uid}", response_model=BookDetailedSchema)
async def get_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    user: User =Depends(role_checker),
):

    book = await book_service.get_book(book_uid, session)

    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@api_router.patch("/{book_uid}", response_model=BookSchema)
async def update_book(
    book_uid: uuid.UUID,
    book_update_data: BookUpdate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(role_checker),
):

    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book is not None:
        return updated_book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@api_router.delete("/{book_uid}")
async def delete_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(role_checker),
):

    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete is not None:  # if book: -> 'False' ,so, else: will trigger
        return None  # Returning 'None' here / handle it
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
