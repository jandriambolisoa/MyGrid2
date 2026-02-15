from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, computed_field
from typing import Optional, List

from backend.config import settings as app_settings
from backend.src.collectibles.schemas import Collectible


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

class UserProfile(BaseModel):
    user: User
    collectibles: Optional[List[Collectible]] = []