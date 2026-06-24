from pydantic import BaseModel, Field
from datetime import datetime, date
import uuid


class UserCreateModel(BaseModel):
    username: str = Field(max_length=12)
    email: str = Field(max_length=40)
    password: str = Field(max_length=20)  # password is not hashed here
    first_name: str
    last_name: str


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = False
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(max_length=20)
