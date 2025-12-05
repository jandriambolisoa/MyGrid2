from typing import List, Optional

from pydantic import BaseModel

from backend.src.registrations.schemas import RegistrationDriver

class ScheduledJob(BaseModel):
    id: str
    name: str
    datetime: str # User friendly datetime

class FrontEndWaitForAction(BaseModel):
    message: str
    redirection: str
    datas: Optional[dict]
