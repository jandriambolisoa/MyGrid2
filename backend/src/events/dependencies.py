from datetime import datetime, UTC
from typing import List, Any, Coroutine

from fastapi.params import Depends

from backend.db.database import get_db
from backend.src.drivers.constants import CODENAME_LENGTH
from backend.src.drivers.exceptions import NotAValidCodenameLengthError, NotAValidColorError, DriverNotFoundError, \
    DriverDoesNotExistsError
from backend.src.events.exceptions import ChampionshipDoesNotExistsError, SessionStartedError, \
    SessionDoesNotExistsError, InvalidDatetimeForSessionCreationError, EventDoesNotExistsError, EventNotFoundError
from backend.src.events.schemas import Event, Championship, Session


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

async def get_upcoming_event(language: str = "en"):
    db = get_db()
    db.cursor.execute("""
        WITH events_translations AS (
            SELECT event_id, name
            FROM eventstranslations
            WHERE language = %s
        )
        SELECT events.id AS id,
        COALESCE(events_translations.name, events.name) AS name,
        events.colors,
        events.flag,
        events.championship_id
        FROM sessions
        LEFT JOIN events ON events.id = event_id
        LEFT JOIN events_translations ON events.id = events_translations.event_id
        WHERE competitive = true 
        AND sessions.datetime > NOW() - INTERVAL '12 hours'
        ORDER BY datetime ASC""", (language,))
    event = db.cursor.fetchone()

    if not event:
        raise EventNotFoundError(language=language)

    return Event(**event)

async def get_last_event_id(language: str = "en"):
    db = get_db()
    db.cursor.execute("""
        SELECT events.id AS id
        FROM sessions
        LEFT JOIN events ON events.id = event_id
        WHERE competitive = true AND datetime < NOW()
        ORDER BY datetime DESC""")
    event = db.cursor.fetchone()

    if not event:
        raise EventNotFoundError(language=language)

    return event["id"]

async def get_event_championship(event_id: int, language: str = "en"):
    db = get_db()
    db.cursor.execute("""\
        SELECT championships.*
        FROM events
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE events.id = %s""", (event_id,))
    championship = db.cursor.fetchone()

    if not championship:
        raise EventNotFoundError(language=language)

    return Championship(**championship)

async def get_session_championship(session_id: int, language: str = "en"):
    db = get_db()
    db.cursor.execute("""\
        SELECT championships.*
        FROM sessions
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE sessions.id = %s""", (session_id,))
    championship = db.cursor.fetchone()

    if not championship:
        raise EventNotFoundError(language=language)

    return Championship(**championship)

async def is_session_over(session_id: int):
    db = get_db()
    db.cursor.execute("""
        SELECT session_id
        FROM sessionsresults
        WHERE session_id = %s""", (session_id,))
    session = db.cursor.fetchone()

    if session:
        return True

    return False

async def get_number_of_races_left(championship_id: int) -> int:
    """
    Returns the number of races left for a given championship id
    Args:
        championship_id: the championship id
        language: for translations (optional)

    Returns:
        int: the number of races left
    """
    db = get_db()
    db.cursor.execute("""\
        WITH races AS (
            SELECT DISTINCT ON (events.name) events.name AS event_name,
            sessions.datetime
            FROM sessions
            LEFT JOIN events ON events.id = sessions.event_id
            LEFT JOIN championships ON championships.id = events.championship_id
            WHERE championship_id = %s AND sessions.competitive = true AND sessions.name = 'Race'
        )
        SELECT races.event_name
        FROM races
        WHERE datetime > NOW()""",(championship_id,))
    races_left = db.cursor.fetchall()

    if not races_left:
        return 0

    return len(races_left)

async def get_number_of_races(championship_id: int) -> int:
    """
    Returns the number of races for a given championship id
    Args:
        championship_id: the championship id
        language: for translations (optional)

    Returns:
        int: the number of races
    """
    db = get_db()
    db.cursor.execute("""\
        SELECT DISTINCT ON (events.name) events.name AS event_name,
        sessions.datetime
        FROM sessions
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE championship_id = %s AND sessions.competitive = true AND sessions.name = 'Race'""", (championship_id,))
    races = db.cursor.fetchall()

    if not races:
        return 0

    return len(races)

async def get_session_full_name(session_id: int, language: str = "en"):
    db = get_db()
    db.cursor.execute("""\
        WITH events_translations AS (
            SELECT event_id, name
            FROM eventstranslations
            WHERE language = %s
        ),
        sessions_translations AS (
            SELECT session_id, name
            FROM sessionstranslations
            WHERE language = %s
        )
        SELECT COALESCE(sessions_translations.name, sessions.name)||' '||COALESCE(events_translations.name, events.name) AS name
        FROM sessions
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN events_translations ON events_translations.event_id = events.id
        LEFT JOIN sessions_translations ON sessions_translations.session_id = sessions.id
        WHERE sessions.id = %s""", (language, language, session_id))
    session = db.cursor.fetchone()

    if not session:
        raise EventNotFoundError(language=language)

    return session["name"]

async def get_session_colors_from_id(session_id: int, language: str = "en") -> List[str]:
    db = get_db()
    db.cursor.execute("""\
        SELECT events.colors
        FROM sessions
        LEFT JOIN events ON events.id = sessions.event_id
        WHERE sessions.id = %s""", (session_id,))
    result = db.cursor.fetchone()

    if not result:
        raise EventNotFoundError(language=language)

    return result["colors"]

async def get_number_of_driver_for_a_session(session_id: int, language: str = "en") -> int:
    db = get_db()
    db.cursor.execute("""\
        SELECT * FROM sessionsregistrations
        WHERE session_id = %s""", (session_id,))
    result = db.cursor.fetchall()

    if result:
        return len(result)
    else:
        return 0

async def get_upcoming_sessions(language: str = "en") -> List[Session]:
    db = get_db()
    db.cursor.execute("""\
        SELECT * FROM sessions
        WHERE datetime > NOW()""")
    sessions = db.cursor.fetchall()

    if not sessions:
        raise EventNotFoundError(language=language)

    return [Session(**session) for session in sessions]


async def get_championship_from_id(championship_id: int, language: str = "en") -> Championship | None:
    db = get_db()
    db.cursor.execute("""\
        SELECT *
        FROM championships
        WHERE id = %s
        """, (championship_id,))
    championship = db.cursor.fetchone()

    if not championship:
        return None

    return Championship(**championship)

async def get_event_from_id(event_id: int, language: str = "en") -> Event | None:
    db = get_db()
    db.cursor.execute("""\
        WITH events_translations AS (
            SELECT event_id, name
            FROM eventstranslations
            WHERE language = %s
        )
        SELECT events.id,
        COALESCE(events_translations.name, events.name) AS name,
        events.colors,
        events.flag,
        events.championship_id
        FROM events
        LEFT JOIN events_translations ON events_translations.event_id = events.id
        WHERE id = %s
        """, (language, event_id))
    event = db.cursor.fetchone()

    if not event:
        return None

    return Event(**event)

async def get_session_from_id(session_id: int, language: str = "en") -> Session:
    db = get_db()
    db.cursor.execute("""\
        SELECT * FROM sessions
        WHERE id = %s""", (session_id,))
    session = db.cursor.fetchone()

    if not session:
        raise EventNotFoundError(language=language)

    session["name"] = await get_session_full_name(session_id, language)

    return Session(**session)
