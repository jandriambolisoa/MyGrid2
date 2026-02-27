from typing import Union, Any

from fastapi import APIRouter, Depends, status
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from starlette.responses import Response

from backend.db.database import Database, get_db
from backend import exceptions as app_exceptions
from backend.oauth2 import get_current_user
from backend.src import predictions
from backend.src.auth.exceptions import UnverifiedUserError
from backend.src.events.dependencies import valid_session_id, valid_session_id_not_started
from backend.src.predictions.exceptions import DriverNotRegisteredForSessionError
from backend.src.scores.algorithms import compute_score
from backend.src.scores.router import get_score_parameters_of_a_championship
from backend.src.users.dependencies import valid_user_id
from backend.src.users.privileges import is_user_moderator_or_admin, is_user_verified
from backend.src.users.schemas import UserSelf
from backend.src.scores import algorithms
from backend.src.predictions.schemas import PredictionSession, PredictionScoreSession, PredictionSessionPost

router = APIRouter(
    prefix="/events/sessions/predictions",
    tags= ["events"]
)

#
# CRUD operations
#

@router.get("/{session_id}", response_model=Union[PredictionSession, PredictionScoreSession], status_code=status.HTTP_200_OK)
async def get_user_prediction(session_id: int = Depends(valid_session_id), user_id: int = Depends(valid_user_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not user_id:
        user_id = current_user.id

    db.cursor.execute("""
        SELECT id, username, created, image
        FROM users
        WHERE id = %s""",(user_id,))
    user = db.cursor.fetchone()

    # Are session results out ?
    db.cursor.execute("""
        SELECT session_id FROM sessionsresults
        WHERE session_id = %s""", (session_id,))
    session_results = db.cursor.fetchone()

    if not session_results:

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
            SELECT drivers.id  AS driver_id, 
            drivers.firstname AS driver_firstname,
            drivers.lastname AS driver_lastname,
            drivers.codename AS driver_codename,
            drivers_team.id AS team_id,
            drivers_team.name AS team_name,
            drivers_team.color AS team_color,
            sessionspredictions.mygrid AS mygrid,
            sessionspredictions.potential AS potential,
            sessions.id AS session_id,
            COALESCE(events_translations.name||' '||sessions_translations.name, events.name||' '||sessions.name) AS session_name,
            sessions.datetime AS session_datetime,
            sessions.event_id AS session_event_id,
            sessions.competitive AS session_competitive,
            events.colors AS session_event_colors
            FROM sessionspredictions
            LEFT JOIN drivers ON drivers.id = sessionspredictions.driver_id
            LEFT JOIN sessions_translations ON sessions_translations.session_id = sessionspredictions.session_id
            LEFT JOIN sessions ON sessions.id = sessionspredictions.session_id
            LEFT JOIN events ON events.id = sessions.event_id
            LEFT JOIN events_translations ON events_translations.event_id = sessions.event_id
            LEFT JOIN drivers_team ON drivers_team.driver_id = drivers.id
            WHERE sessionspredictions.session_id = %s AND sessionspredictions.user_id = %s
            ORDER BY sessionspredictions.mygrid ASC;""", (language, language, session_id, session_id, user_id))
        results = db.cursor.fetchall()
    else:

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
            sessionspredictions.mygrid AS mygrid,
            sessionspredictions.potential AS potential,
            sessions.id AS session_id,
            COALESCE(events_translations.name||' '||sessions_translations.name, events.name||' '||sessions.name) AS session_name,
            sessions.datetime AS session_datetime,
            sessions.event_id AS session_event_id,
            sessions.competitive AS session_competitive,
            events.colors AS session_event_colors,
            sessionsresults.result AS result,
            scores.score AS score,
            COALESCE(events_translations.name||' '||sessions_translations.name, events.name||' '||sessions.name) AS session_name
            FROM sessionspredictions
            LEFT JOIN drivers ON drivers.id = sessionspredictions.driver_id
            LEFT JOIN sessionsresults ON sessionsresults.driver_id = sessionspredictions.driver_id
            LEFT JOIN scores ON scores.driver_id = sessionspredictions.driver_id
            LEFT JOIN sessions_translations ON sessions_translations.session_id = sessionspredictions.session_id
            LEFT JOIN sessions ON sessions.id = sessionspredictions.session_id
            LEFT JOIN events ON events.id = sessions.event_id
            LEFT JOIN events_translations ON events_translations.event_id = sessions.event_id
            LEFT JOIN drivers_team ON drivers_team.driver_id = drivers.id
            WHERE sessionspredictions.session_id = %s
            AND sessionsresults.session_id = %s
            AND sessionspredictions.user_id = %s
            AND scores.session_id = %s
            AND scores.user_id = %s
            ORDER BY sessionspredictions.mygrid ASC;""", (language, language, session_id, session_id, session_id, user_id, session_id, user_id))
        results = db.cursor.fetchall()

    if not results:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # Convert result into PredictionSession or PredictionScoreSession schemas
    predictions = list()
    session_potential = 0
    session_score = 0
    for result in results:
        driver = {key.removeprefix("driver_"): result[key] for key in result.keys() if
                  key.startswith("driver_")}
        team = {key.removeprefix("team_"): result[key] for key in result.keys() if
                  key.startswith("team_")}

        if not session_results:
            predictions.append({
                "driver": driver,
                "team": team,
                "mygrid": result["mygrid"],
                "potential": result["potential"]
            })
        else:
            predictions.append({
                "driver": driver,
                "team": team,
                "mygrid": result["mygrid"],
                "result": result["result"],
                "score": result["score"]
            })
            session_score += result["score"]

        session_potential += result["potential"]

    session = {key.removeprefix("session_"): results[0][key] for key in results[0].keys() if
               key.startswith("session_")}
    session["potential"] = session_potential

    if not session_results:
        return {
            "session": session,
            "user": user,
            "predictions": predictions,
            "session_potential": session_potential
        }
    else:
        session["score"] = session_score
        return {
            "session": session,
            "user": user,
            "predictions": predictions
        }


@router.post("/{session_id}", status_code=status.HTTP_201_CREATED)
async def create_my_grid(session_id: int, session_predictions: PredictionSessionPost, language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_verified(current_user.id):
        raise UnverifiedUserError(language=language)

    session_id = await valid_session_id_not_started(session_id, language=language)

    # Override already existing predictions
    await delete_my_grid(session_id, language, db, current_user)

    db.cursor.execute("""
        SELECT driver_id, prediction
        FROM sessionsregistrations
        WHERE session_id = %s""", (session_id,))
    grid = db.cursor.fetchall()
    grid_size = len(grid)
    grid_predictions = {item["driver_id"]: item["prediction"] for item in grid}

    db.cursor.execute("""
        SELECT championships.id
        FROM sessions
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE sessions.id = %s;""", (session_id,))
    championship = db.cursor.fetchone()

    score_parameters = await get_score_parameters_of_a_championship(
        championship["id"],
        db=db,
        current_user=current_user
    )

    for prediction in session_predictions.predictions:
        score_potential = await compute_score(
            user_driver_prediction=prediction.mygrid,
            mygrid_driver_prediction=grid_predictions[prediction.driver_id],
            driver_result=prediction.mygrid,
            grid_size=grid_size,
            parameters=score_parameters
        )

        db.cursor.execute("""
            INSERT INTO sessionspredictions (session_id, user_id, driver_id, mygrid, potential)
            VALUES (%s, %s, %s, %s, %s)""", (session_id, current_user.id, prediction.driver_id, prediction.mygrid, score_potential))

    try:
        db.conn.commit()
    except ForeignKeyViolation:
        db.conn.rollback()
        raise DriverNotRegisteredForSessionError(language=language)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_grid(session_id: int, language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_verified(current_user.id):
        raise UnverifiedUserError(language=language)

    session_id = await valid_session_id_not_started(session_id, language=language)

    db.cursor.execute("""
        DELETE FROM sessionspredictions
        WHERE session_id = %s AND user_id = %s""", (session_id, current_user.id))
    db.conn.commit()
