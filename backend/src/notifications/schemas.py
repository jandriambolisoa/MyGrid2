from pydantic import BaseModel
from typing import List, Optional

class PushToken(BaseModel):
    token: str

class PushNotification(BaseModel):
    title: str
    body: str