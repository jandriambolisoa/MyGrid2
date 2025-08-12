from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from backend.src.auth import constants


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    created: datetime
    image: Optional[str]

class UserCreate(BaseModel):
    username: str = Field(min_length= constants.USERNAME_MIN_LENGTH, max_length=constants.USERNAME_MAX_LENGTH)
    password: str = Field(min_length= constants.PW_MIN_LENGTH)
    email: EmailStr
    language: Optional[str] = Field(default= "en")
    image: Optional[str]

class UserSelf(BaseModel):
    id: int
    username: str
    email: EmailStr
    created: datetime
    modified: datetime
    language: str
    image: Optional[str]

class TokenData(BaseModel):
    username: str
    language: str