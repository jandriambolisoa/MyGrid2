from pydantic import BaseModel
from typing import Optional

class Team(BaseModel):
    id: int
    name: str
    color: str
    image: Optional[str] = None

class Driver(BaseModel):
    id: int
    firstname: str
    lastname: str
    codename: str
    racing_number: int
    team: Team
    image: Optional[str] = None