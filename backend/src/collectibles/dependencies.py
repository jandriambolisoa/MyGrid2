from typing import List

from fastapi import Depends
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from backend.db.database import get_db
from backend.oauth2 import get_current_user
from backend.src.collectibles.schemas import Collectible
from backend.src.users.schemas import UserSelf


async def get_user_collectibles(user_id: int = None, current_user: UserSelf = Depends(get_current_user)) -> List[Collectible] | None:

    db = get_db()
    db.cursor.execute("""\
        SELECT collectibles.name,
        collectibles.description,
        userscollectibles.created,
        userscollectibles.views,
        userscollectibles.user_id AS owner_id
        FROM userscollectibles
        LEFT JOIN collectibles ON collectibles.id = userscollectibles.collectible_id
        WHERE userscollectibles.user_id = %s""", (user_id,))
    collectibles = db.cursor.fetchall()

    if not collectibles:
        return []

    return [Collectible(**collectible) for collectible in collectibles]

async def distribute_collectible(user_id: int, collectible_id: int):
    db = get_db()
    try:
        db.cursor.execute("""\
            INSERT INTO userscollectibles (user_id, collectible_id)
            VALUES (%s, %s)""", (user_id, collectible_id))
        db.conn.commit()

    except ForeignKeyViolation:
        db.conn.rollback()

    except UniqueViolation:
        db.conn.rollback()