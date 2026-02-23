from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, computed_field
from typing import Optional

from backend.config import settings as app_settings

class Collectible(BaseModel):
    name: str
    description: str
    created: Optional[datetime] = None
    views: Optional[int] = None
    owner_id: Optional[int] = None

    @computed_field
    @property
    def model(self) -> str:
        if not self.owner_id:
            return f"{app_settings.api_url}/collectibles/{self.name}/model"
        else:
            return f"{app_settings.api_url}/collectibles/{self.name}/model?owner_id={self.owner_id}"

    @computed_field
    @property
    def textures(self) -> str:
        return f"{app_settings.api_url}/collectibles/{self.name}/textures"

    @computed_field
    @property
    def icon(self) -> str:
        return f"{app_settings.api_url}/collectibles/{self.name}/icon"
