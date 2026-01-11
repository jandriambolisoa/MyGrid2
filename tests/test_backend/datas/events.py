import random
from datetime import datetime, timedelta, UTC

from backend.db.database import get_db
from backend.src.events.schemas import Championship, Event, Session
from backend.utils import random_color

def create_championship(name: str) -> Championship:
    db = get_db()
    db.cursor.execute("""
        INSERT INTO championships (name)
        VALUES (%s)
        RETURNING *
        """, (name,))
    new = db.cursor.fetchone()

    return Championship(**new)

def create_event(name: str, championship_id: int):
    db = get_db()
    db.cursor.execute("""
        INSERT INTO events (name, color, championship_id)
        VALUES (%s, %s, %s)
        RETURNING *
        """, (name, random_color(), championship_id))
    new = db.cursor.fetchone()

    return Event(**new)

def create_session(name: str, event_id: int, competitive: bool, upcoming: bool = True):
    if upcoming:
        random_datetime = datetime.now(UTC) + timedelta(hours=random.choice(range(9, 99)))
    else:
        random_datetime = datetime.now(UTC) - timedelta(hours=random.choice(range(9, 99)))

    db = get_db()
    db.cursor.execute("""
        INSERT INTO sessions (name, datetime, event_id, competitive)
        VALUES (%s, %s, %s, %s)
        RETURNING *
        """, (name, random_datetime, event_id, competitive))
    new = db.cursor.fetchone()

    return Session(**new)


def get_competitive_sessions_from_event_id(event_id: int):
    db = get_db()
    db.cursor.execute("""
        SELECT *
        FROM sessions
        WHERE event_id = %s AND competitive = true""", (event_id,))
    results = db.cursor.fetchall()

    return [Session(**res) for res in results]