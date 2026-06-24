# Database models

from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
import uuid

"""
Use default_factory: Here's a function that creates a value. Inside a field() but inside column use default
"""


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,            # In my python code its a UUID obj but in database store this column as PosgreSQL's native UUID
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
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )

    # Representation method
    def __repr__(self):
        return f"<Book {self.title}>"
