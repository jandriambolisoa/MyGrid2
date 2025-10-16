from pydantic import BaseModel
from typing import List, Optional

from backend.src.drivers.schemas import Driver, Team
from backend.src.events.schemas import Session
from backend.src.users.schemas import User


class PredictionPost(BaseModel):
    driver_id: int
    mygrid: int

class PredictionSessionPost(BaseModel):
    predictions: List[PredictionPost]

class Prediction(BaseModel):
    driver: Driver
    mygrid: int
    potential: int

class PredictionSession(BaseModel):
    session_name: str
    user: User
    predictions: List[Prediction]
    session_potential: int

class PredictionScore(BaseModel):
    driver: Driver
    mygrid: int
    result: int
    score: int

class PredictionScoreSession(BaseModel):
    session_name: str
    user: User
    predictions: List[PredictionScore]
    session_potential: int
    session_score: int