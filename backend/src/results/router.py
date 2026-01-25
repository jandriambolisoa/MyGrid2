from fastapi import APIRouter, Depends, status
from psycopg.errors import UniqueViolation, ForeignKeyViolation

from backend.db.database import Database, get_db
from backend import exceptions as app_exceptions
from backend.oauth2 import get_current_user
from backend.src.events.dependencies import valid_session_id
from backend.src.results.exceptions import NoResultsFoundError, InvalidSessionResultsAttemptError
from backend.src.results.schemas import ResultSession, ResultPost
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
async def get_session_results(session_id: int = Depends(valid_session_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
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
        )
        SELECT drivers.id AS driver_id,
        drivers.firstname AS driver_firstname,
        drivers.lastname AS driver_lastname,
        drivers.codename AS driver_codename,
        sessionsresults.result AS result,
        sessionsresults.points AS points,
        COALESCE(events_translations.name||' '||sessions_translations.name, events.name||' '||sessions.name) AS session_name
        FROM sessionsresults
        LEFT JOIN drivers ON drivers.id = sessionsresults.driver_id
        LEFT JOIN sessions_translations ON sessions_translations.session_id = sessionsresults.session_id
        LEFT JOIN sessions ON sessions.id = sessionsresults.session_id
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN events_translations ON events_translations.event_id = sessions.event_id
        WHERE sessionsresults.session_id = %s
        ORDER BY sessionsresults.result ASC;""", (language, language, session_id))
    results = db.cursor.fetchall()

    if not results:
        raise NoResultsFoundError(language=language)

    # Convert results into Result schemas
    driver_results = list()
    for result in results:
        driver = {key.removeprefix("driver_"): result[key] for key in result.keys() if
                  key.startswith("driver_")}

        driver_results.append({
            "driver": driver,
            "result": result["result"],
            "points": result["points"]
        })

    return {
        "session_name": results[0]["session_name"],
        "results": driver_results
    }


@router.post("/{session_id}", status_code=status.HTTP_201_CREATED)
async def override_session_results(results: list[ResultPost], session_id: int = Depends(valid_session_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise app_exceptions.ForbiddenAccessException(language=language)

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
async def remove_session_results(session_id: int = Depends(valid_session_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise app_exceptions.ForbiddenAccessException(language=language)

    db.cursor.execute("""
        DELETE FROM sessionsresults
        WHERE session_id = %s""", (session_id,))
    db.conn.commit()

    await results_signals.delete_session_results.send(session_id=session_id, user=current_user)
