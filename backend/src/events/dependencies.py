from fastapi.params import Depends

from backend.db.database import get_db
from backend.src.drivers.constants import CODENAME_LENGTH
from backend.src.drivers.exceptions import NotAValidCodenameLengthError, NotAValidColorError, DriverNotFoundError, \
    DriverDoesNotExistsError
from backend.src.events.exceptions import ChampionshipDoesNotExistsError, SessionStartedError, SessionDoesNotExistsError


async def valid_championship_id(id: int, language: str = "en") -> int:
    db = get_db()
    db.cursor.execute("""
        SELECT id FROM championships
        WHERE id = %s""", (id,))
    championship = db.cursor.fetchone()
    if not championship:
        raise ChampionshipDoesNotExistsError(language=language, championship_id=id)

    return id


async def valid_event_id(id: int, language: str = "en") -> int:
    db = get_db()
    db.cursor.execute("""
        SELECT id FROM events
        WHERE id = %s""", (id,))
    event = db.cursor.fetchone()
    if not event:
        raise ChampionshipDoesNotExistsError(language=language, event_id=id)

    return id


async def valid_session_id(id: int, language: str = "en") -> int:
    db = get_db()
    db.cursor.execute("""
        SELECT id FROM sessions
        WHERE id = %s""", (id,))
    session = db.cursor.fetchone()
    if not session:
        raise SessionDoesNotExistsError(language=language, session_id=id)

    return id

async def valid_session_id_not_started(id: Depends(valid_session_id), language: str = "en"):
    db = get_db()
    db.cursor.execute("""
        SELECT sessions.datetime
        FROM sessions
        WHERE sessions.id = %s
        AND datetime > NOW()
    """, (id,))
    valid_session = db.cursor.fetchone()

    if not valid_session:
        raise SessionStartedError(language=language)

