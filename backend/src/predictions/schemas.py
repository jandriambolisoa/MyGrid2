from pydantic import BaseModel
from typing import List, Optional

from pydantic_core.core_schema import computed_field

from backend.src.drivers.schemas import Driver, Team
from backend.src.events.schemas import Session
from backend.src.reactions.schemas import UserReaction
from backend.src.users.schemas import User


class PredictionPost(BaseModel):
    driver_id: int
    mygrid: int

class PredictionSessionPost(BaseModel):
    predictions: List[PredictionPost]

class SessionWithPotential(Session):
    potential: int
    score: Optional[int] = 0
    reactions: Optional[List[UserReaction]] = None

class PredictionPreview(BaseModel):
    user: User
    sessions: List[SessionWithPotential]

class Prediction(BaseModel):
    driver: Driver
    team: Team
    mygrid: int
    potential: int

class PredictionSession(BaseModel):
    session: SessionWithPotential
    user: User
    predictions: List[Prediction]

class PredictionScore(BaseModel):
    driver: Driver
    team: Team
    mygrid: int
    result: int
    score: int

class PredictionScoreSession(BaseModel):
    session: SessionWithPotential
    user: User
    predictions: List[PredictionScore]
