from typing import List, Optional

from pydantic import BaseModel

from backend.src.users.schemas import User
from backend.src.events.schemas import Championship, Event, Session


class UserRank(BaseModel):
    rank: int
    user: User
    score: int

class UserSessionRank(BaseModel):
    rank: int
    user: User
    event: Event
    session: Session
    score: int

class ChampionshipRanks(BaseModel):
    championship: Championship
    viewer_rank: UserRank
    ranks: List[UserRank]

class EventRanks(BaseModel):
    championship: Championship
    event: Event
    viewer_rank: UserRank
    ranks: List[UserRank]

class SessionRanks(BaseModel):
    championship: Championship
    ranks: List[UserSessionRank]
