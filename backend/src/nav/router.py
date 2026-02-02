from fastapi import APIRouter, Depends, status

from backend.db.database import Database, get_db
from backend.oauth2 import get_current_user
from backend.src.events.dependencies import valid_championship_id, get_upcoming_event,\
    is_session_over, get_event_championship
from backend.src.nav.schemas import NavMainEvent, NavMainEventSession
from backend.src.predictions.dependencies import is_user_has_prono
from backend.src.users.schemas import UserSelf
from backend.utils import get_nice_datetime

router = APIRouter(
    prefix="/nav",
    tags= ["nav"]
)

#
# CRUD operations
#

@router.get("/home/main-event", response_model=NavMainEvent, status_code=status.HTTP_200_OK)
async def home_get_main_event(championship_id: int = Depends(valid_championship_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    event = await get_upcoming_event(language)
    championship = await get_event_championship(event.id, language)

    db.cursor.execute("""
        WITH sessions_translations AS (
            SELECT session_id, name
            FROM sessionstranslations
            WHERE language = %s
        )
        SELECT sessions.id,
        COALESCE(sessions_translations.name, sessions.name) AS name,
        sessions.datetime,
        sessions.competitive,
        sessions.event_id
        FROM sessions
        LEFT JOIN sessions_translations ON sessions_translations.session_id = sessions.id
        WHERE event_id = %s
        ORDER BY datetime ASC""", (language, event.id))
    sessions = db.cursor.fetchall()
    sessions_to_return = list()

    for session in sessions:
        has_prono = await is_user_has_prono(current_user.id, session["id"])
        nice_datetime= get_nice_datetime(session["datetime"], language)
        is_over= await is_session_over(session["id"])

        if is_over:
            db.cursor.execute("""\
                SELECT COALESCE(SUM(score), 0) AS total
                FROM scores
                WHERE user_id = %s
                AND session_id = %s""", (current_user.id, session["id"]))
            score_to_display = db.cursor.fetchone()
        else:
            db.cursor.execute("""\
                SELECT COALESCE(SUM(potential), 0) AS total
                FROM sessionspredictions
                WHERE user_id = %s
                AND session_id = %s""", (current_user.id, session["id"]))
            score_to_display = db.cursor.fetchone()

        session["has_prono"] = has_prono
        session["nice_datetime"] = nice_datetime
        session["is_over"] = is_over
        session["score"] = score_to_display["total"]

        sessions_to_return.append(NavMainEventSession(**session))

    return {
        "championship": championship,
        "event": event,
        "sessions": sessions_to_return
    }
