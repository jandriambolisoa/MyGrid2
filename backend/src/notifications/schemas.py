from pydantic import BaseModel, EmailStr
from typing import List, Optional

class PushToken(BaseModel):
    token: str
    language: Optional[str] = "en"

class PushNotification(BaseModel):
    title: dict # {'language': 'text'}
    body: dict # {'language': 'text'}

class UserEmail(BaseModel):
    email: EmailStr
    username: str
    language: Optional[str] = "en"

class SimpleEmail(BaseModel):
    subject: dict # {'language': 'text'}
    preview: dict # {'language': 'text'}
    image_url: str
    body: dict # {'language': 'text'}
    title: dict # {'language': 'text'}