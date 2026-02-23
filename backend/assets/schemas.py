from pydantic import BaseModel


class RenameAsset(BaseModel):
    old_name: str
    new_name: str