from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from typing import List, Optional
from datetime import datetime, date
import uuid


"""
Previously we simply created out database connection & table using a lifespan event, But we need a way to perform migrations in our database (Alembic)
(alembic allows us to make changes to our database without having to drop any tables or modify or delete anything in our database)
"""


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = False  # False initialy
    password_hash: str = Field(
        exclude=True
    )  # exclude = True , while Serializaion it omits this field
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )

    # Since a user can have a list of books // use Quotes in "Book" (cuz its not defined yet, forward reference)
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )  # lazyloading

    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )  # lazyloading

    def __repr__(self):
        return f"<User {self.username}>"


# Database models
"""
Use default_factory: Here's a function that creates a value. Inside a field() but inside column use default
"""


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,  # In my python code its a UUID obj but in database store this column as PosgreSQL's native UUID
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
    )
    title: str
    author: str
    genre: str
    published_year: date
    language: str
    pagecount: int
    user_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.uid"
    )  # to do it in "SQLAlchemy" way: from sqlalchemy import ForeignKey , ForeignKey("user.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )

    # Lazy loading - "Left Outer Join" - to avoid a N+1 Query 
    user: Optional["User"] = Relationship(
        back_populates="books", sa_relationship_kwargs={"lazy": "joined"}
    )

    # Use "selectin" for one-to-many relationships (like reviews in Book)
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )

    # Representation method
    def __repr__(self):
        return f"<Book {self.title}>"


# Reviews Table


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    rating: int = Field(le=5, ge=1)
    review_text: str = Field(max_length=1000)
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for {self.book_uid} by {self.user_uid}>"



''' Stor Time in UTC

# Import timezone from datetime
from datetime import datetime, timezone

# Use timezone-aware UTC datetime
created_at: datetime = Field(
    sa_column=Column(pg.TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
)

'''