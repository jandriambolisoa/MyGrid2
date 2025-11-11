from fastapi import APIRouter, status, Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from backend.db.database import get_db, Database
from backend.exceptions import ForbiddenAccessException
from backend.oauth2 import get_current_user
from backend import exceptions as app_exceptions
from backend.constants import QUERY_LIMIT
from backend.src.events.dependencies import valid_championship_id, valid_session_id, valid_event_id
from backend.src.events.exceptions import ChampionshipAlreadyExistsError, EventAlreadyExistsError, \
    SessionAlreadyExistsError, EventNotFoundError, ChampionshipNotFoundError, SessionNotFoundError
from backend.src.events.schemas import Championship, ChampionshipCreate, Event, EventCreate, Session, SessionCreate, \
    EventSearch, ChampionshipUpdate, EventUpdate, SessionUpdate
from backend.src.users.privileges import is_user_moderator_or_admin
from backend.src.events import signals as events_signal
from backend.src.users.schemas import UserSelf
from backend.translations import valid_translations

router = APIRouter(
    prefix="/events",
    tags= ["events"]
)

#
# CRUD operations
#

@router.post("/championships", status_code=status.HTTP_201_CREATED, response_model=Championship)
async def create_championship(championship: ChampionshipCreate, language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    try:
        db.cursor.execute("""
            INSERT INTO championships (name)
            VALUES (%s)
            RETURNING *
        """, (championship.name.title(),))
        created = db.cursor.fetchone()

        db.conn.commit()
    except UniqueViolation:
        raise ChampionshipAlreadyExistsError(language=language)

    events_signal.create_championship.send(created, user=current_user)
    return created


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Event)
async def create_event(to_create: EventCreate, language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    translations = await valid_translations(to_create.name, language=language)

    try:
        db.cursor.execute("""
            INSERT INTO events (name, championship_id, color)
            VALUES (%s, %s, %s)
            RETURNING *""", (to_create.name["en"].title(), to_create.championship_id, to_create.color))
        created = db.cursor.fetchone()

        for lang in translations:
            db.cursor.execute("""
                INSERT INTO eventstranslations (event_id, language, name)
                VALUES (%s, %s, %s)""", (created["id"], lang, translations[lang].title()))

        db.conn.commit()
    except UniqueViolation:
        raise EventAlreadyExistsError(language=language)

    events_signal.create_event.send(created, user=current_user)
    return created

@router.post("/sessions", status_code=status.HTTP_201_CREATED, response_model=Session)
async def create_session(to_create: SessionCreate, language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    translations = await valid_translations(to_create.name, language=language)

    try:
        db.cursor.execute("""
            INSERT INTO sessions (name, datetime, event_id)
            VALUES (%s, %s, %s)
            RETURNING *""", (to_create.name["en"].title(), to_create.datetime, to_create.event_id))
        created = db.cursor.fetchone()

        for lang in translations:
            db.cursor.execute("""
                INSERT INTO sessionstranslations (session_id, language, name)
                VALUES (%s, %s, %s)""", (created["id"], lang, translations[lang].title()))

        db.conn.commit()
    except UniqueViolation:
        raise SessionAlreadyExistsError(language=language)

    events_signal.create_session.send(created, user=current_user)
    return created


@router.get("/search", response_model=list[EventSearch])
async def search_event(db:Database = Depends(get_db),
        language: str = "en",
        q: str = "",
        limit: int = QUERY_LIMIT,
        page: int = 0):

    search = "%" + q + "%"
    offset = limit * page

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
        SELECT sessions.id AS session_id,
        COALESCE(sessions_translations.name, sessions.name) AS session_name,
        sessions.datetime AS session_datetime,
        sessions.competitive AS session_competitive,
        events.id AS event_id,
        COALESCE(events_translations.name, events.name) AS event_name,
        events.color AS event_color,
        championships.id AS championship_id,
        championships.name AS championship_name
        FROM sessions
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN events_translations ON events.id = events_translations.event_id
        LEFT JOIN sessions_translations ON sessions.id = sessions_translations.session_id
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE LOWER(COALESCE(events_translations.name, events.name))
        LIKE LOWER(%s)
        LIMIT %s OFFSET %s;""", (language, language, search, limit, offset))
    results = db.cursor.fetchall()

    if not results:
        raise EventNotFoundError(language=language)

    # Convert result into EventSearch schemas
    search_results = dict()
    for result in results:
        championship = {key.removeprefix("championship_"): result[key] for key in result.keys() if key.startswith("championship_")}
        event = {key.removeprefix("event_"): result[key] for key in result.keys() if key.startswith("event_") or key == 'championship_id'}
        session = {key.removeprefix("session_"): result[key] for key in result.keys() if key.startswith("session_") or key == 'event_id'}

        if event["id"] not in search_results.keys():
            search_results[event["id"]] = {**event}
            search_results[event["id"]]["championship"] = {**championship}
            search_results[event["id"]]["sessions"] = [session]
        else:
            search_results[event["id"]]["sessions"].append(session)

    return list(search_results.values())


@router.put("/championship/{id}", response_model=Championship)
async def update_championship(datas: ChampionshipUpdate, id: int = Depends(valid_championship_id), language: str = "en", db:Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    # Get orig championship
    db.cursor.execute("""\
        SELECT * FROM championships
        WHERE id = %s""", (id,))
    orig = db.cursor.fetchone()

    # Get default values
    if not datas.name:
        datas.name = orig["name"]

    try:
        db.cursor.execute("""\
            UPDATE championships
            SET name = %s
            WHERE id = %s
            RETURNING *
            """, (datas.name, id))
        updated = db.cursor.fetchone()
        db.conn.commit()

    except UniqueViolation:
        db.conn.rollback()
        raise ChampionshipAlreadyExistsError(language=language)

    return updated


@router.put("/sessions/{id}", response_model=Championship)
async def update_session(datas: SessionUpdate, id: int = Depends(valid_session_id), language: str = "en", db:Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    # Get orig event
    db.cursor.execute("""\
        SELECT * FROM sessions
        WHERE id = %s""", (id,))
    orig = db.cursor.fetchone()

    # Get default values
    if not datas.name:
        datas.name = orig["name"]
    else:
        datas.name = orig["name"] | datas.name
    if not datas.datetime:
        datas.datetime = orig["datetime"]

    try:
        db.cursor.execute("""\
            UPDATE sessions
            SET name = %s, datetime = %s
            WHERE id = %s
            RETURNING *
            """, (datas.name, datas.datetime, id))
        updated = db.cursor.fetchone()
        db.conn.commit()

    except UniqueViolation:
        db.conn.rollback()
        raise SessionAlreadyExistsError(language=language)

    return updated


@router.put("/{id}", response_model=Championship)
async def update_event(datas: EventUpdate, id: int = Depends(valid_event_id), language: str = "en", db:Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    # Get orig event
    db.cursor.execute("""\
        SELECT * FROM events
        WHERE id = %s""", (id,))
    orig = db.cursor.fetchone()

    # Get default values
    if not datas.name:
        datas.name = orig["name"]
    else:
        datas.name = orig["name"] | datas.name
    if not datas.color:
        datas.color = orig["color"]

    try:
        db.cursor.execute("""\
            UPDATE events
            SET name = %s, color = %s
            WHERE id = %s
            RETURNING *
            """, (datas.name, datas.color, id))
        updated = db.cursor.fetchone()
        db.conn.commit()

    except UniqueViolation:
        db.conn.rollback()
        raise EventAlreadyExistsError(language=language)

    return updated


@router.delete("/championships/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_championship(id: int = Depends(valid_championship_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    db.cursor.execute("""
        DELETE FROM championships
        WHERE id = %s
        RETURNING *""", (id,))
    to_delete = db.cursor.fetchone()

    db.conn.commit()
    events_signal.delete_championship.send(to_delete, user = current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/sessions/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(id: int = Depends(valid_session_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    db.cursor.execute("""
        DELETE FROM sessions
        WHERE id = %s
        RETURNING *""", (id,))
    to_delete = db.cursor.fetchone()

    db.conn.commit()
    events_signal.delete_session.send(to_delete, user = current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(id: int = Depends(valid_event_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    db.cursor.execute("""
        DELETE FROM events
        WHERE id = %s
        RETURNING *""", (id,))
    to_delete = db.cursor.fetchone()

    db.conn.commit()
    events_signal.delete_event.send(to_delete, user = current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

