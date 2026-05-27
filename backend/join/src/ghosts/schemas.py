from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, computed_field
from typing import Optional, List

from backend.config import settings as app_settings
from backend.src.collectibles.schemas import Collectible

class GhostUserCreate(BaseModel):
    username: str
    image: Optional[str] = None
