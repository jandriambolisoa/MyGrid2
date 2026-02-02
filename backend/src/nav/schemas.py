from pydantic import BaseModel
from typing import List, Optional

from backend.src.drivers.schemas import Driver, Team
from backend.src.events.schemas import Session, Championship, Event, EventCollectible
from backend.src.users.schemas import User

class NavMainEventSession(Session):
    nice_datetime: str
    has_prono: bool
    is_over: bool
    score: int

class NavMainEvent(BaseModel):
    championship: Championship
    event: Event
    sessions: List[NavMainEventSession]
