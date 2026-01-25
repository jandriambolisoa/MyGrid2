from datetime import datetime, UTC

from fastapi.params import Depends

from backend.db.database import get_db
from backend.src.drivers.constants import CODENAME_LENGTH
from backend.src.drivers.exceptions import NotAValidCodenameLengthError, NotAValidColorError, DriverNotFoundError, \
    DriverDoesNotExistsError
from backend.src.events.exceptions import ChampionshipDoesNotExistsError, SessionStartedError, \
    SessionDoesNotExistsError, InvalidDatetimeForSessionCreationError


async def valid_championship_id(championship_id: int, language: str = "en") -> int:
    db = get_db()
    db.cursor.execute("""
        SELECT id FROM championships
        WHERE id = %s""", (championship_id,))
    championship = db.cursor.fetchone()
    if not championship:
        raise ChampionshipDoesNotExistsError(language=language, championship_id=championship_id)

    return championship_id


async def valid_event_id(event_id: int, language: str = "en") -> int:
    db = get_db()
    db.cursor.execute("""
        SELECT id FROM events
        WHERE id = %s""", (event_id,))
    event = db.cursor.fetchone()
    if not event:
        raise ChampionshipDoesNotExistsError(language=language, event_id=event_id)

    return event_id


async def valid_session_id(session_id: int, language: str = "en") -> int:
    db = get_db()
    db.cursor.execute("""
        SELECT id FROM sessions
        WHERE id = %s""", (session_id,))
    session = db.cursor.fetchone()
    if not session:
        raise SessionDoesNotExistsError(language=language, session_id=session_id)

    return session_id

async def valid_session_id_not_started(session_id: int = Depends(valid_session_id), language: str = "en"):
    db = get_db()
    db.cursor.execute("""
        SELECT sessions.datetime
        FROM sessions
        WHERE sessions.id = %s
        AND sessions.datetime > NOW()
    """, (session_id,))
    valid_session = db.cursor.fetchone()

    if not valid_session:
        raise SessionStartedError(language=language)

    return session_id

async def valid_session_creation_datetime(datetime: datetime, language: str = "en"):
    if datetime < datetime.now(UTC):
        raise InvalidDatetimeForSessionCreationError(language=language)

    return datetime
