from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from backend.src.auth import constants


class User(BaseModel):
    id: int
    username: str
    created: datetime
    image: Optional[str]

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    image: Optional[str] = None

class UserSelf(BaseModel):
    id: int
    username: str
    email: EmailStr
    created: datetime
    modified: datetime
    language: Optional[str] = "en"
    image: Optional[str] = None
