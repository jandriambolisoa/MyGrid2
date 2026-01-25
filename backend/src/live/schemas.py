from typing import List, Optional

from pydantic import BaseModel

from backend.src.registrations.schemas import RegistrationDriver

class LiveDatas(RegistrationDriver):
    position: int
    lap_duration: Optional[str]  # formated as minute:seconds.milliseconds
    interval: Optional[float]  # in seconds
