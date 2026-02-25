from pydantic import BaseModel
from typing import List, Optional

class PushToken(BaseModel):
    token: str
    language: Optional[str] = "en"

class PushNotification(BaseModel):
    title: dict # {'language': 'text'}
    body: dict # {'language': 'text'}