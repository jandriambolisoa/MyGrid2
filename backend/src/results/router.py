from fastapi import APIRouter, Depends, status
from psycopg.errors import UniqueViolation, ForeignKeyViolation

from backend.db.database import Database, get_db
from backend import exceptions as app_exceptions
from backend.oauth2 import get_current_user
from backend.src.events.dependencies import valid_session_id, get_number_of_driver_for_a_session
from backend.src.results.exceptions import NoResultsFoundError, InvalidSessionResultsAttemptError, \
    IncorrectNumberOfDriverError
from backend.src.results.schemas import ResultSession, ResultPost
from backend.src.users.dependencies import get_current_user_language
from backend.src.users.privileges import is_user_moderator_or_admin
from backend.src.users.schemas import UserSelf
from backend.src.results import signals as results_signals

router = APIRouter(
    prefix="/events/sessions/results",
    tags= ["events"]
)

#
# CRUD operations
#

@router.get("/{session_id}", response_model=ResultSession)
async def get_session_results(session_id: int = Depends(valid_session_id), language: str = Depends(get_current_user_language), db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    db.cursor.execute("""
        WITH events_translations AS (
            SELECT event_id, name
            FROM eventstranslations
            WHERE language = %s
        ),
        sessions_translations AS (
            SELECT session_id, name
            FROM sessionstranslations
            WHERE language = %s
        ),
        drivers_team AS (
            SELECT sessionsregistrations.driver_id,
            teams.id,
            teams.name,
            teams.color
            FROM sessionsregistrations
            LEFT JOIN teams ON teams.id = sessionsregistrations.team_id
            WHERE sessionsregistrations.session_id = %s
        )
        SELECT drivers.id AS driver_id,
        drivers.firstname AS driver_firstname,
        drivers.lastname AS driver_lastname,
        drivers.codename AS driver_codename,
        drivers_team.id AS team_id,
        drivers_team.name AS team_name,
        drivers_team.color AS team_color,
        sessionsresults.result AS result,
        sessionsresults.points AS points,
        sessions.id AS session_id,
        COALESCE(events_translations.name||' '||sessions_translations.name, events.name||' '||sessions.name) AS session_name,
        sessions.datetime AS session_datetime,
        sessions.event_id AS session_event_id,
        sessions.competitive AS session_competitive
        FROM sessionsresults
        LEFT JOIN drivers ON drivers.id = sessionsresults.driver_id
        LEFT JOIN sessions_translations ON sessions_translations.session_id = sessionsresults.session_id
        LEFT JOIN sessions ON sessions.id = sessionsresults.session_id
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN events_translations ON events_translations.event_id = sessions.event_id
        INNER JOIN drivers_team ON drivers_team.driver_id = drivers.id
        WHERE sessionsresults.session_id = %s
        ORDER BY sessionsresults.result ASC;""", (language, language, session_id, session_id))
    results = db.cursor.fetchall()

    if not results:
        raise NoResultsFoundError(language=language)

    # Convert results into Result schemas
    driver_results = list()
    for result in results:
        driver = {key.removeprefix("driver_"): result[key] for key in result.keys() if
                  key.startswith("driver_")}
        team = {key.removeprefix("team_"): result[key] for key in result.keys() if
                key.startswith("team_")}

        driver_results.append({
            "driver": driver,
            "team": team,
            "result": result["result"],
            "points": result["points"]
        })

    session = {key.removeprefix("session_"): results[0][key] for key in results[0].keys() if
               key.startswith("session_")}

    return {
        "session": session,
        "results": driver_results
    }


@router.post("/{session_id}", status_code=status.HTTP_201_CREATED)
async def override_session_results(results: list[ResultPost], session_id: int = Depends(valid_session_id), language: str = Depends(get_current_user_language), db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise app_exceptions.ForbiddenAccessException(language=language)

    # Refuse to override session results if the number of driver doesn't correspond
    if not len(results) == await get_number_of_driver_for_a_session(session_id):
        raise IncorrectNumberOfDriverError(language)

    # Remove old session results
    db.cursor.execute("""
        DELETE FROM sessionsresults
        WHERE session_id = %s""", (session_id,))
    db.conn.commit()

    try:
        for result in results:
            db.cursor.execute("""
                INSERT INTO sessionsresults (session_id, driver_id, result, points)
                VALUES (%s, %s, %s, %s)""",(session_id, result.driver_id, result.result, result.points))

        db.conn.commit()

        await results_signals.updated_session_results.send(session_id=session_id, user=current_user)

    except ForeignKeyViolation:
        db.conn.rollback()
        raise InvalidSessionResultsAttemptError(language=language)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_session_results(session_id: int = Depends(valid_session_id), language: str = Depends(get_current_user_language), db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise app_exceptions.ForbiddenAccessException(language=language)

    db.cursor.execute("""
        DELETE FROM sessionsresults
        WHERE session_id = %s""", (session_id,))
    db.conn.commit()

    await results_signals.delete_session_results.send(session_id=session_id, user=current_user)
