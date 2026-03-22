from typing import List, Optional

from pydantic import BaseModel

from backend.src.events.schemas import Session
from backend.src.users.schemas import User

class PostReaction(BaseModel):
    reaction: str

class UserReaction(BaseModel):
    user: User
    reaction: str