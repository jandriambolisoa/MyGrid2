from fastapi import APIRouter, Depends, status
from psycopg.errors import UniqueViolation, ForeignKeyViolation

from backend.db.database import Database, get_db
from backend import exceptions as app_exceptions
from backend.oauth2 import get_current_user
from backend.src.events.dependencies import valid_session_id, valid_session_id_not_started
from backend.src.registrations.exceptions import NoRegistrationsFoundError, RegistrationAlreadyExistsError, \
    InvalidSessionRegistrationAttemptError, RegistrationCannotSwapWithAlreadyRegisteredDriverError
from backend.src.registrations.schemas import RegistrationDriver, RegistrationSession, RegistrationPost, \
    RegistrationSwapDrivers, RegistrationSwapTeams
from backend.src.users.privileges import is_user_moderator_or_admin
from backend.src.users.schemas import UserSelf
from backend.src.registrations import signals as registrations_signals

router = APIRouter(
    prefix="/events/sessions/registrations",
    tags= ["events"]
)

#
# CRUD operations
#

@router.get("/{session_id}", response_model=RegistrationSession)
async def get_session_registrations(session_id: int = Depends(valid_session_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
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
        teams.id AS team_id,
        teams.name AS team_name,
        teams.color AS team_color,
        sessionsregistrations.prediction AS prediction,
        COALESCE(events_translations.name||' '||sessions_translations.name, events.name||' '||sessions.name) AS session_name
        FROM sessionsregistrations
        LEFT JOIN drivers ON drivers.id = sessionsregistrations.driver_id
        LEFT JOIN teams ON teams.id = sessionsregistrations.team_id
        LEFT JOIN sessions_translations ON sessions_translations.session_id = sessionsregistrations.session_id
        LEFT JOIN sessions ON sessions.id = sessionsregistrations.session_id
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN events_translations ON events_translations.event_id = sessions.event_id
        WHERE sessionsregistrations.session_id = %s
        ORDER BY sessionsregistrations.prediction;""", (language, language, session_id))
    results = db.cursor.fetchall()

    if not results:
        raise NoRegistrationsFoundError(language=language)

    # Convert result into RegistrationDriver schemas
    registrations = list()
    for result in results:
        driver = {key.removeprefix("driver_"): result[key] for key in result.keys() if
                        key.startswith("driver_")}
        team = {key.removeprefix("team_"): result[key] for key in result.keys() if
                 key.startswith("team_")}
        prediction = result["prediction"]

        registrations.append({
            "driver": driver,
            "team": team,
            "driver_id": driver["id"],
            "team_id": team["id"],
            "prediction": prediction
        })

    return {
        "session_name": results[0]["session_name"],
        "registrations": registrations
    }


@router.post("/{session_id}", status_code=status.HTTP_201_CREATED)
async def override_session_registrations(registrations: list[RegistrationPost], session_id: int = Depends(valid_session_id_not_started), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise app_exceptions.ForbiddenAccessException(language=language)

    # Remove old session registrations
    db.cursor.execute("""
        DELETE FROM sessionsregistrations
        WHERE session_id = %s""", (session_id,))
    db.conn.commit()

    try:
        for registration in registrations:
            db.cursor.execute("""
                INSERT INTO sessionsregistrations (session_id, driver_id, team_id, prediction)
                VALUES (%s, %s, %s, %s)""",(session_id, registration.driver_id, registration.team_id, registration.prediction))

        db.conn.commit()

        await registrations_signals.updated_session_registrations.send(session_id=session_id, user=current_user)

    except ForeignKeyViolation:
        db.conn.rollback()
        raise InvalidSessionRegistrationAttemptError(language=language)


@router.put("/{session_id}/swap-drivers", status_code=status.HTTP_200_OK)
async def swap_a_driver_with_an_unregistered_driver(
        drivers: RegistrationSwapDrivers,
        session_id: int = Depends(valid_session_id_not_started),
        db: Database = Depends(get_db),
        language: str = "en",
        current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise app_exceptions.ForbiddenAccessException(language=language)

    # Get the original drivers registrations for this session
    # and update every drivers' predictions.
    db.cursor.execute("""
        SELECT driver_id, team_id, prediction
        FROM sessionsregistrations
        WHERE session_id = %s
        ORDER BY prediction ASC""", (session_id,))
    drivers_list = db.cursor.fetchall()

    if not drivers_list:
        raise NoRegistrationsFoundError(language=language)

    predictions = {d["driver_id"]: d["prediction"] for d in drivers_list}

    if drivers.new_driver_id in predictions.keys():
        raise RegistrationCannotSwapWithAlreadyRegisteredDriverError(language=language)

    to_remove = None
    for driver in drivers_list:
        if driver["prediction"] <= drivers.new_driver_prediction and driver["prediction"] > predictions[drivers.old_driver_id]:
            driver["prediction"] = driver["prediction"] - 1
        elif driver["prediction"] >= drivers.new_driver_prediction and driver["prediction"] < predictions[drivers.old_driver_id]:
            driver["prediction"] = driver["prediction"] + 1
        elif driver["prediction"] == predictions[drivers.old_driver_id]:
            to_remove = driver

    # Add the new driver and remove the old one inside the original list and use
    # the result of this operation to recreate sessionsregistrations table entries.
    drivers_list.remove(to_remove)
    drivers_list.append({
        "driver_id": drivers.new_driver_id,
        "team_id": to_remove["team_id"],
        "prediction": drivers.new_driver_prediction
    })

    db.cursor.execute("""
        DELETE
        FROM sessionsregistrations
        WHERE session_id = %s""", (session_id,))

    try:
        for driver in drivers_list:
            db.cursor.execute("""
                INSERT INTO sessionsregistrations (session_id, driver_id, team_id, prediction)
                VALUES (%s, %s, %s, %s)
                """, (session_id, driver["driver_id"], driver["team_id"], driver["prediction"]))

        db.conn.commit()
    except:
        db.conn.rollback()
        raise InvalidSessionRegistrationAttemptError(language=language)

    # Update the new driver in users sessions predictions
    db.cursor.execute("""
        UPDATE sessionspredictions
        SET driver_id = %s
        WHERE driver_id = %s
        AND session_id = %s""", (drivers.new_driver_id, drivers.old_driver_id, session_id))
    db.conn.commit()

    await registrations_signals.updated_session_registrations.send(session_id=session_id, user=current_user)


@router.put("/{session_id}/swap-teams", status_code=status.HTTP_200_OK)
async def swap_teams_between_two_drivers(
        drivers: RegistrationSwapTeams,
        session_id: int = Depends(valid_session_id_not_started),
        db: Database = Depends(get_db),
        language: str = "en",
        current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise app_exceptions.ForbiddenAccessException(language=language)

    db.cursor.execute("""
        SELECT team_id
        FROM sessionsregistrations
        WHERE session_id = %s AND driver_id = %s""", (session_id, drivers.driver_id_1))
    driver_1 = db.cursor.fetchone()

    db.cursor.execute("""
        SELECT team_id
        FROM sessionsregistrations
        WHERE session_id = %s AND driver_id = %s""", (session_id, drivers.driver_id_2))
    driver_2 = db.cursor.fetchone()

    if not driver_1 or not driver_2:
        raise NoRegistrationsFoundError(language=language)

    db.cursor.execute("""
        UPDATE sessionsregistrations
        SET team_id = %s
        WHERE session_id = %s AND driver_id = %s""",(driver_2["team_id"], session_id, drivers.driver_id_1))

    db.cursor.execute("""
        UPDATE sessionsregistrations
        SET team_id = %s
        WHERE session_id = %s AND driver_id = %s;""",(driver_1["team_id"], session_id, drivers.driver_id_2))

    db.conn.commit()

    await registrations_signals.updated_session_registrations.send(session_id=session_id, user=current_user)