from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, computed_field
from typing import Optional, List

from backend.config import settings as app_settings
from backend.db.database import get_db
from backend.src.collectibles.schemas import Collectible
from backend.src.users.schemas import User

class League(BaseModel):
    id: int
    name: str
    description: datetime
    colors: List[str]
    created: datetime

    @computed_field
    @property
    def size(self) -> int:
        db = get_db()
        db.cursor.execute("""\
            SELECT COUNT(*)
            FROM leaguesusers
            WHERE  league_id = %s""", (self.id,))
        return db.cursor.fetchone()[0]

    @computed_field
    @property
    def organizers(self) -> List[User]:
        db = get_db()
        db.cursor.execute("""\
            SELECT users.id AS id,
            users.username AS username,
            users.created AS created,
            users.image AS image
            FROM leaguesusers
            WHERE league_id = %s
            AND organizer = true""", (self.id,))
        return db.cursor.fetchall()
