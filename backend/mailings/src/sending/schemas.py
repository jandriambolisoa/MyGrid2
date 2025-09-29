from fastapi import UploadFile
from pydantic import BaseModel

class EmailDatas(BaseModel):
    receiver: str
    subject: str
    fields: dict