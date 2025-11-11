from pydantic import BaseModel
from typing import List, Optional

from backend.src.drivers.schemas import Driver, Team
from backend.src.events.schemas import Session


class RegistrationPost(BaseModel):
    driver_id: int
    team_id: int
    prediction: int

class RegistrationDriver(RegistrationPost):
    driver: Driver
    team: Team
    prediction: int

class RegistrationSession(BaseModel):
    session_name: str
    registrations: List[RegistrationDriver]

class RegistrationSwapDrivers(BaseModel):
    old_driver_id: int
    new_driver_id: int
    new_driver_prediction: int

class RegistrationSwapTeams(BaseModel):
    driver_id_1: int
    driver_id_2: int