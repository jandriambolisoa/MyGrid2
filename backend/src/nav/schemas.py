from pydantic import BaseModel
from typing import List, Optional

from backend.src.drivers.schemas import Driver, Team
from backend.src.events.schemas import Session, Championship, Event
from backend.src.ranks.schemas import DriverChampionshipLeaderboard, TeamChampionshipLeaderboard
from backend.src.users.schemas import User

class NavMainEventSession(Session):
    has_prono: bool
    is_over: bool
    score: int

class NavMainEvent(BaseModel):
    championship: Championship
    event: Event
    sessions: List[NavMainEventSession]

class NavDriverChampionshipLeaderboard(BaseModel):
    leaderboard: DriverChampionshipLeaderboard
    has_prono: bool

class NavTeamChampionshipLeaderboard(BaseModel):
    leaderboard: TeamChampionshipLeaderboard
    has_prono: bool

class NavChampionship(BaseModel):
    championship: Championship
    wdc: NavDriverChampionshipLeaderboard
    wcc: NavTeamChampionshipLeaderboard