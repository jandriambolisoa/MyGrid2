from fastapi import APIRouter, status, Depends, Response
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from backend.db.database import get_db, Database
from backend.exceptions import ForbiddenAccessException, UnexpectedError
from backend.oauth2 import get_current_user
from backend.constants import QUERY_LIMIT
from backend.src.drivers.schemas import DriverRegistration
from backend.src.events.constants import WDC_PREDICTION_POINTS, WCC_PREDICTION_POINTS
from backend.src.events.dependencies import valid_championship_id, valid_session_id, valid_event_id, \
    valid_session_creation_datetime, get_number_of_races_left, get_number_of_races, get_session_full_name, \
    get_event_championship, get_session_championship
from backend.src.events.exceptions import ChampionshipAlreadyExistsError, EventAlreadyExistsError, \
    SessionAlreadyExistsError, EventNotFoundError, ChampionshipNotFoundError, SessionNotFoundError, \
    ChampionshipDoesNotExistsError, TooLateToMakeAChampionshipPrediction
from backend.src.events.schemas import Championship, ChampionshipCreate, Event, EventCreate, Session, SessionCreate, \
    EventSearch, ChampionshipUpdate, EventUpdate, SessionUpdate, WDCPrediction, \
    WCCPrediction, PredictionWCCPotentialResponse, PredictionWDCPotentialResponse, SessionDrivers
from backend.src.predictions.dependencies import is_user_has_prono
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
        db.conn.rollback()
        raise ChampionshipAlreadyExistsError(language=language)

    await events_signal.create_championship.send(created, user=current_user)
    return created


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Event)
async def create_event(to_create: EventCreate, language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    translations = await valid_translations(to_create.name, language=language)

    try:
        db.cursor.execute("""
            INSERT INTO events (name, championship_id, color, flag)
            VALUES (%s, %s, %s, %s)
            RETURNING *""", (to_create.name["en"].title(), to_create.championship_id, to_create.color, to_create.flag))
        created = db.cursor.fetchone()

        for lang in translations:
            db.cursor.execute("""
                INSERT INTO eventstranslations (event_id, language, name)
                VALUES (%s, %s, %s)""", (created["id"], lang, translations[lang].title()))

        db.conn.commit()
    except UniqueViolation:
        db.conn.rollback()
        raise EventAlreadyExistsError(language=language)

    await events_signal.create_event.send(created, user=current_user)
    return created

@router.post("/sessions", status_code=status.HTTP_201_CREATED, response_model=Session)
async def create_session(to_create: SessionCreate, language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    datetime = await valid_session_creation_datetime(to_create.datetime, language=language)
    translations = await valid_translations(to_create.name, language=language)

    try:
        db.cursor.execute("""
            INSERT INTO sessions (name, datetime, event_id, competitive)
            VALUES (%s, %s, %s, %s)
            RETURNING *""", (to_create.name["en"].title(), datetime, to_create.event_id, to_create.competitive))
        created = db.cursor.fetchone()

        for lang in translations:
            db.cursor.execute("""
                INSERT INTO sessionstranslations (session_id, language, name)
                VALUES (%s, %s, %s)""", (created["id"], lang, translations[lang].title()))

        db.conn.commit()
    except UniqueViolation:
        db.conn.rollback()
        raise SessionAlreadyExistsError(language=language)

    await events_signal.create_session.send(Session(**created), user=current_user)
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


@router.put("/championships/{championship_id}", response_model=Championship)
async def update_championship(datas: ChampionshipUpdate, championship_id: int = Depends(valid_championship_id), language: str = "en", db:Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    # Get orig championship
    db.cursor.execute("""\
        SELECT * FROM championships
        WHERE id = %s""", (championship_id,))
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
            """, (datas.name, championship_id))
        updated = db.cursor.fetchone()
        db.conn.commit()

    except UniqueViolation:
        db.conn.rollback()
        raise ChampionshipAlreadyExistsError(language=language)

    return updated


@router.put("/sessions/{session_id}", response_model=Championship)
async def update_session(datas: SessionUpdate, session_id: int = Depends(valid_session_id), language: str = "en", db:Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    # Get orig event
    db.cursor.execute("""\
        SELECT * FROM sessions
        WHERE id = %s""", (session_id,))
    orig = db.cursor.fetchone()

    # Get default values
    translations = None
    if not datas.name:
        datas.name["en"] = orig["name"]
    else:
        translations = await valid_translations(datas.name, language=language)
        datas.name["en"] =  datas.name.get("en", orig["name"])
    if not datas.datetime:
        datas.datetime = orig["datetime"]

    try:
        db.cursor.execute("""\
            UPDATE sessions
            SET name = %s, datetime = %s
            WHERE id = %s
            RETURNING *
            """, (datas.name["en"], datas.datetime, session_id))
        updated = db.cursor.fetchone()

        for lang in translations:
            db.cursor.execute("""
                UPDATE sessionstranslations
                SET name = %s
                WHERE session_id = %s AND language = %s""", (translations[lang].title(), session_id, lang))

        db.conn.commit()

    except UniqueViolation:
        db.conn.rollback()
        raise SessionAlreadyExistsError(language=language)

    return updated


@router.put("/{event_id}", response_model=Championship)
async def update_event(datas: EventUpdate, event_id: int = Depends(valid_event_id), language: str = "en", db:Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    # Get orig event
    db.cursor.execute("""\
        SELECT * FROM events
        WHERE id = %s""", (event_id,))
    orig = db.cursor.fetchone()

    # Get default values
    translations = None
    if not datas.name:
        datas.name["en"] = orig["name"]
    else:
        translations = await valid_translations(datas.name, language=language)
        datas.name["en"] = datas.name.get("en", orig["name"])
    if not datas.color:
        datas.color = orig["color"]
    if not datas.flag:
        datas.flag = orig["flag"]

    try:
        db.cursor.execute("""\
            UPDATE events
            SET name = %s, color = %s, flag = %s, collectible = %s, collectibletextures = %s
            WHERE id = %s
            RETURNING *
            """, (datas.name["en"], datas.color, datas.flag, datas.collectible.model, datas.collectible.textures, event_id))
        updated = db.cursor.fetchone()

        for lang in translations:
            db.cursor.execute("""
                UPDATE eventstranslations
                SET name = %s
                WHERE event_id = %s AND language = %s""", (translations[lang].title(), event_id, lang))

        db.conn.commit()

    except UniqueViolation:
        db.conn.rollback()
        raise EventAlreadyExistsError(language=language)

    return updated


@router.delete("/championships/{championship_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_championship(championship_id: int = Depends(valid_championship_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    db.cursor.execute("""
        DELETE FROM championships
        WHERE id = %s
        RETURNING *""", (championship_id,))
    to_delete = db.cursor.fetchone()

    db.conn.commit()
    await events_signal.delete_championship.send(to_delete, user = current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: int = Depends(valid_session_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    db.cursor.execute("""
        DELETE FROM sessions
        WHERE id = %s
        RETURNING *""", (session_id,))
    to_delete = db.cursor.fetchone()

    db.conn.commit()
    await events_signal.delete_session.send(Session(**to_delete), user = current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int = Depends(valid_event_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    db.cursor.execute("""
        DELETE FROM events
        WHERE id = %s
        RETURNING *""", (event_id,))
    to_delete = db.cursor.fetchone()

    db.conn.commit()
    await events_signal.delete_event.send(to_delete, user = current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/championships/{championship_id}/wdc-prediction", response_model=PredictionWDCPotentialResponse)
async def override_wdc_prediction(prediction: WDCPrediction, championship_id: int = Depends(valid_championship_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    races_total = await get_number_of_races(championship_id)
    races_left = await get_number_of_races_left(championship_id)

    if not races_total:
        raise ChampionshipDoesNotExistsError(championship_id, language)

    if not races_left:
        raise TooLateToMakeAChampionshipPrediction(language)

    potential = round(WDC_PREDICTION_POINTS * races_left / races_total)

    db.cursor.execute("""\
        SELECT potential FROM wdcpredictions
        WHERE user_id = %s AND championship_id = %s""", (current_user.id, championship_id))
    has_prono = db.cursor.fetchone()

    if has_prono:
        db.cursor.execute("""\
            WITH prediction AS (
                UPDATE wdcpredictions
                SET driver_id = %s, potential = %s
                WHERE user_id = %s AND championship_id = %s
                RETURNING *
            )
            SELECT drivers.id AS driver_id,
            drivers.firstname AS driver_firstname,
            drivers.lastname AS driver_lastname,
            drivers.codename AS driver_codename,
            potential
            FROM prediction
            LEFT JOIN drivers ON drivers.id = prediction.driver_id""", (prediction.driver_id, potential, current_user.id, championship_id))
        try:
            db.conn.commit()
        except ForeignKeyViolation:
            db.conn.rollback()
            raise UnexpectedError(language)

        prediction = db.cursor.fetchone()

        return {
            "driver": {key.removeprefix("driver_"): prediction[key] for key in prediction.keys() if
                       key.startswith("driver_")},
            "potential": prediction["potential"]
        }
    else:
        db.cursor.execute("""\
            WITH prediction AS (
                INSERT INTO wdcpredictions (user_id, championship_id, driver_id, potential)
                VALUES (%s, %s, %s, %s)
                RETURNING *
            )
            SELECT drivers.id AS driver_id,
            drivers.firstname AS driver_firstname,
            drivers.lastname AS driver_lastname,
            drivers.codename AS driver_codename,
            potential
            FROM prediction
            LEFT JOIN drivers ON drivers.id = prediction.driver_id""", (current_user.id, championship_id, prediction.driver_id, potential))
        try:
            db.conn.commit()
        except ForeignKeyViolation:
            db.conn.rollback()
            raise UnexpectedError(language)

        prediction = db.cursor.fetchone()

        return {
            "driver": {key.removeprefix("driver_"): prediction[key] for key in prediction.keys() if
                       key.startswith("driver_")},
            "potential": prediction["potential"]
        }

@router.post("/championships/{championship_id}/wcc-prediction", response_model=PredictionWCCPotentialResponse)
async def override_wcc_prediction(prediction: WCCPrediction, championship_id: int = Depends(valid_championship_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    races_total = await get_number_of_races(championship_id)
    races_left = await get_number_of_races_left(championship_id)

    if not races_total:
        raise ChampionshipDoesNotExistsError(championship_id, language)

    if not races_left:
        raise TooLateToMakeAChampionshipPrediction(language)

    potential = round(WCC_PREDICTION_POINTS * races_left / races_total)

    db.cursor.execute("""\
        SELECT potential FROM wccpredictions
        WHERE user_id = %s AND championship_id = %s""", (current_user.id, championship_id))
    has_prono = db.cursor.fetchone()

    if has_prono:
        db.cursor.execute("""\
            WITH prediction AS (
                UPDATE wccpredictions
                SET team_id = %s, potential = %s
                WHERE user_id = %s AND championship_id = %s
                RETURNING *
            )
            SELECT teams.id AS team_id,
            teams.name AS team_name,
            teams.color AS team_color,
            potential
            FROM prediction
            LEFT JOIN teams ON teams.id = prediction.team_id""", (prediction.team_id, potential, current_user.id, championship_id))
        try:
            db.conn.commit()
        except ForeignKeyViolation:
            db.conn.rollback()
            raise UnexpectedError(language)

        prediction = db.cursor.fetchone()

        return {
            "team": {key.removeprefix("team_"): prediction[key] for key in prediction.keys() if
                       key.startswith("team_")},
            "potential": prediction["potential"]
        }
    else:
        db.cursor.execute("""\
            WITH prediction AS (
                INSERT INTO wccpredictions (user_id, championship_id, team_id, potential)
                VALUES (%s, %s, %s, %s)
                RETURNING *
            )
            SELECT teams.id AS team_id,
            teams.name AS team_name,
            teams.color AS team_color,
            potential
            FROM prediction
            LEFT JOIN teams ON teams.id = prediction.team_id""", (current_user.id, championship_id, prediction.team_id, potential))
        try:
            db.conn.commit()
        except ForeignKeyViolation:
            db.conn.rollback()
            raise UnexpectedError(language)

        prediction = db.cursor.fetchone()

        return {
            "team": {key.removeprefix("team_"): prediction[key] for key in prediction.keys() if
                       key.startswith("team_")},
            "potential": prediction["potential"]
        }

@router.get("/sessions/{session_id}/drivers", response_model=SessionDrivers, status_code=status.HTTP_200_OK)
async def get_session_drivers(session_id: int = Depends(valid_session_id), championship_order: bool = False, language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    """
    Will try to return drivers in the order of the user prediction for a session,
    otherwise will return drivers in the global prediction order.
    If championship_order is True, will return drivers in the current championship standings order.
    Args:
        session_id: the id of the session
        championship_order: if True, will return drivers in the championship standings order.
        language: language of errors
        db: the db
        current_user: current user schema

    Returns:
        SessionDrivers schema
    """
    session_name = await get_session_full_name(session_id, language)
    championship = await get_session_championship(session_id, language)
    has_prono = await is_user_has_prono(current_user.id, session_id)

    if not has_prono and not championship_order:
        db.cursor.execute("""\
            SELECT drivers.id AS driver_id, 
            drivers.firstname AS driver_firstname,
            drivers.lastname AS driver_lastname,
            drivers.codename AS driver_codename,
            teams.id AS team_id,
            teams.name AS team_name,
            teams.color AS team_color,
            sessionsregistrations.prediction
            FROM sessionsregistrations
            LEFT JOIN drivers ON drivers.id = sessionsregistrations.driver_id
            LEFT JOIN teams ON teams.id = sessionsregistrations.team_id
            WHERE session_id = %s
            ORDER BY prediction ASC""", (session_id,))
        drivers = db.cursor.fetchall()

    elif has_prono and not championship_order:
        db.cursor.execute("""\
            SELECT drivers.id AS driver_id, 
            drivers.firstname AS driver_firstname,
            drivers.lastname AS driver_lastname,
            drivers.codename AS driver_codename,
            teams.id AS team_id,
            teams.name AS team_name,
            teams.color AS team_color,
            sessionsregistrations.prediction,
            sessionspredictions.mygrid
            FROM sessionspredictions
            LEFT JOIN sessionsregistrations ON sessionsregistrations.driver_id = sessionspredictions.driver_id
            LEFT JOIN drivers ON drivers.id = sessionsregistrations.driver_id
            LEFT JOIN teams ON teams.id = sessionsregistrations.team_id
            WHERE sessionsregistrations.session_id = %s AND sessionspredictions.session_id = %s AND sessionspredictions.user_id = %s
            ORDER BY sessionspredictions.mygrid ASC""", (session_id, session_id, current_user.id))
        drivers = db.cursor.fetchall()

    elif not has_prono and championship_order:
        db.cursor.execute("""\
            WITH session_registration AS (
                SELECT drivers.id AS driver_id, 
                drivers.firstname AS driver_firstname,
                drivers.lastname AS driver_lastname,
                drivers.codename AS driver_codename,
                teams.id AS team_id,
                teams.name AS team_name,
                teams.color AS team_color,
                sessionsregistrations.prediction
                FROM sessionsregistrations
                LEFT JOIN drivers ON drivers.id = sessionsregistrations.driver_id
                LEFT JOIN teams ON teams.id = sessionsregistrations.team_id
                WHERE session_id = %s
            )
            SELECT session_registration.driver_id,
            session_registration.driver_firstname,
            session_registration.driver_lastname,
            session_registration.driver_codename,
            session_registration.team_id,
            session_registration.team_name,
            session_registration.team_color,
            session_registration.prediction,             
            SUM(sessionsresults.points) AS score
            FROM sessionsresults
            LEFT JOIN session_registration ON session_registration.driver_id = sessionsresults.driver_id
            LEFT JOIN sessions ON sessions.id = sessionsresults.session_id
            LEFT JOIN events ON events.id = sessions.event_id
            LEFT JOIN championships ON championships.id = events.championship_id
            WHERE championships.id = %s
            GROUP BY session_registration.driver_id,
            session_registration.driver_firstname,
            session_registration.driver_lastname,
            session_registration.driver_codename,
            session_registration.team_id,
            session_registration.team_name,
            session_registration.team_color,
            session_registration.prediction
            ORDER BY score DESC""", (session_id, championship.id))
        drivers = db.cursor.fetchall()

    else:
        db.cursor.execute("""\
            WITH session_registration AS (
                SELECT drivers.id AS driver_id, 
            drivers.firstname AS driver_firstname,
            drivers.lastname AS driver_lastname,
            drivers.codename AS driver_codename,
            teams.id AS team_id,
            teams.name AS team_name,
            teams.color AS team_color,
            sessionsregistrations.prediction,
            sessionspredictions.mygrid
            FROM sessionspredictions
            LEFT JOIN sessionsregistrations ON sessionsregistrations.driver_id = sessionspredictions.driver_id
            LEFT JOIN drivers ON drivers.id = sessionsregistrations.driver_id
            LEFT JOIN teams ON teams.id = sessionsregistrations.team_id
            WHERE sessionsregistrations.session_id = %s AND sessionspredictions.session_id = %s AND sessionspredictions.user_id = %s
            )
            SELECT session_registration.driver_id,
            session_registration.driver_firstname,
            session_registration.driver_lastname,
            session_registration.driver_codename,
            session_registration.team_id,
            session_registration.team_name,
            session_registration.team_color,
            session_registration.prediction,
            session_registration.mygrid,
            SUM(sessionsresults.points) AS score
            FROM sessionsresults
            LEFT JOIN session_registration ON session_registration.driver_id = sessionsresults.driver_id
            LEFT JOIN sessions ON sessions.id = sessionsresults.session_id
            LEFT JOIN events ON events.id = sessions.event_id
            LEFT JOIN championships ON championships.id = events.championship_id
            WHERE championships.id = %s
            GROUP BY session_registration.driver_id,
            session_registration.driver_firstname,
            session_registration.driver_lastname,
            session_registration.driver_codename,
            session_registration.team_id,
            session_registration.team_name,
            session_registration.team_color,
            session_registration.prediction,
            session_registration.mygrid
            ORDER BY score DESC""", (session_id, session_id, current_user.id, championship.id))
        drivers = db.cursor.fetchall()

    return {
        "session_name": session_name,
        "drivers": [{
            "driver": {key.removeprefix("driver_"): driver[key] for key in driver.keys() if key.startswith("driver_")},
            "team": {key.removeprefix("team_"): driver[key] for key in driver.keys() if key.startswith("team_")},
            "prediction": driver["prediction"],
            "mygrid": None if not has_prono else driver["mygrid"]
        } for driver in drivers]
    }