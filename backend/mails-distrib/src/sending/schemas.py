from pydantic import BaseModel

class EmailDatas(BaseModel):
    receiver: str
    subject: str
    content: str