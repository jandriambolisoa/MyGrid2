from pydantic import BaseModel
from typing import Optional

class FrontEndWaitForAction(BaseModel):
    message: str
    redirection: str
    datas: Optional[dict]
