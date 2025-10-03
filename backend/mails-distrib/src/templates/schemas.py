from pydantic import BaseModel

class Content(BaseModel):
    filename: str
    html: str