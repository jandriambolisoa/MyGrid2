from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class Championship(BaseModel):
    id: int
    name: str

class ChampionshipCreate(BaseModel):
    name: str

class ChampionshipUpdate(BaseModel):
    name: Optional[str] = None

class EventCollectible(BaseModel):
    model: str
    textures: Optional[str] = None

class Event(BaseModel):
    id: int
    name: str
    championship_id: int
    color: str
    flag: str
    collectible: Optional[str] = None
    collectibletextures: Optional[str] = None

class EventCreate(BaseModel):
    name: dict # {language: translation}
    championship_id: int
    color: str
    flag: str

class EventUpdate(BaseModel):
    name: Optional[dict] = None # {language: translation}
    color: Optional[str] = None
    flag: Optional[str] = None
    collectible: Optional[EventCollectible] = None

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
