from pydantic import BaseModel
from typing import List, Optional

from backend.src.drivers.schemas import Driver, Team
from backend.src.events.schemas import Session


class ResultPost(BaseModel):
    driver_id: int
    result: int
    points: int

class Result(BaseModel):
    driver: Driver
    team: Team
    result: int
    points: int

class ResultSession(BaseModel):
    session: Session
    results: List[Result]
