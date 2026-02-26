from typing import List, Optional

from pydantic import BaseModel

class Driver(BaseModel):
    id: int
    firstname: str
    lastname: str
    codename: str

class DriverCreate(BaseModel):
    firstname: str
    lastname: str
    codename: str

class DriverUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    codename: Optional[str] = None

class Team(BaseModel):
    id: int
    name: str
    color: str

class TeamCreate(BaseModel):
    name: str
    color: str

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None

class DriversTeams(Driver):
    teams: List[Team]

class TeamsDrivers(Team):
    drivers: List[Driver]
