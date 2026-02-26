from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class AppStatus(BaseModel):
    version: str
    maintenance: bool
    notes: Optional[str] = None
    created: datetime