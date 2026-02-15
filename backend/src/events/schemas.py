from datetime import datetime
from pydantic import BaseModel, computed_field
from typing import List, Optional

from backend.config import settings as app_settings
from backend.src.drivers.schemas import Driver, Team, DriverRegistration


class Championship(BaseModel):
    id: int
    name: str

    @computed_field
    @property
    def trophee_model(self) -> str:
        return f"{app_settings.api_url}/collectibles/championship_{self.id:04d}/model"

    @computed_field
    @property
    def trophee_textures(self) -> str:
        return f"{app_settings.api_url}/collectibles/championship_{self.id:04d}/textures"

    @computed_field
    @property
    def trophee_icon(self) -> str:
        return f"{app_settings.api_url}/collectibles/championship_{self.id:04d}/icon"

class ChampionshipCreate(BaseModel):
    name: str

class ChampionshipUpdate(BaseModel):
    name: Optional[str] = None

class Event(BaseModel):
    id: int
    name: str
    championship_id: int
    color: str
    flag: str

    @computed_field
    @property
    def trophee_model(self) -> str:
        return f"{app_settings.api_url}/collectibles/event_{self.id:04d}/model"

    @computed_field
    @property
    def trophee_textures(self) -> str:
        return f"{app_settings.api_url}/collectibles/event_{self.id:04d}/textures"

    @computed_field
    @property
    def trophee_icon(self) -> str:
        return f"{app_settings.api_url}/collectibles/event_{self.id:04d}/icon"


class EventCreate(BaseModel):
    name: dict # {language: translation}
    championship_id: int
    color: str
    flag: str

class EventUpdate(BaseModel):
    name: Optional[dict] = None # {language: translation}
    color: Optional[str] = None
    flag: Optional[str] = None

class Session(BaseModel):
    id: int
    name: str
    datetime: datetime
    event_id: int
    competitive: bool

class SessionCreate(BaseModel):
    name: dict # {language: translation}
    datetime: datetime
    event_id: int
    competitive: bool

class SessionUpdate(BaseModel):
    name: Optional[dict] = None # {language: translation}
    datetime: Optional[datetime] = None

class EventSearch(Event):
    championship: Championship
    sessions: List[Session]

class WDCPrediction(BaseModel):
    driver_id: int

class WCCPrediction(BaseModel):
    team_id: int

class PredictionWDCPotentialResponse(BaseModel):
    driver: Driver
    potential: int

class PredictionWCCPotentialResponse(BaseModel):
    team: Team
    potential: int

class SessionDrivers(BaseModel):
    session_name: str
    drivers: List[DriverRegistration]