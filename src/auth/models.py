from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime

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

    def __repr__(self):
        return f"<User {self.username}"
