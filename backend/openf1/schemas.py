from typing import Optional
from pydantic import BaseModel

class Driver(BaseModel):
    number: int
    codename: str

class DriverLive(BaseModel):
    position: int
    lap_duration: Optional[float] #in seconds
    interval: Optional[float] #in seconds
    driver: Driver