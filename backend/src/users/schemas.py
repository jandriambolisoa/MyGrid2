from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, computed_field
from typing import Optional, List

from backend.config import settings as app_settings
from backend.src.collectibles.schemas import Collectible


class User(BaseModel):
    id: int
    username: str
    created: datetime
    image: Optional[str] = None

    @computed_field
    @property
    def image_url(self) -> str:
        if self.image:
            return f"{app_settings.api_url}/images/{self.image}"
        else:
            return str()


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    image: Optional[str] = None

class UserConvertFromGhost(BaseModel):
    password: str
    email: str

class UserSelf(BaseModel):
    id: int
    username: str
    email: EmailStr
    created: datetime
    modified: datetime
    language: Optional[str] = "en"
    image: Optional[str] = None

    @computed_field
    @property
    def image_url(self) -> str:
        if self.image:
            return f"{app_settings.api_url}/images/{self.image}"
        else:
            return str()

class UserProfile(BaseModel):
    user: User
    collectibles: Optional[List[Collectible]] = []