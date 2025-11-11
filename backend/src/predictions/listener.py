from backend.db.database import get_db
from backend.src.registrations.signals import updated_session_registrations
from backend.src.scores.router import get_score_parameters_of_a_championship
from backend.src.users.schemas import UserSelf
from backend.src.scores.algorithms import compute_score


@updated_session_registrations.connect
async def update_users_predictions_potential(session_id: int, user: UserSelf):
    db = get_db()

    db.cursor.execute("""
        SELECT sessionspredictions.user_id AS user_id,
        sessionspredictions.driver_id AS driver_id,
        sessionspredictions.mygrid AS mygrid,
        sessionsregistrations.prediction AS prediction
        FROM sessionspredictions
        LEFT JOIN sessionsregistrations ON sessionsregistrations.driver_id = sessionspredictions.driver_id
        WHERE sessionspredictions.session_id = %s
        AND sessionsregistrations.session_id = %s""", (session_id, session_id))
    predictions = db.cursor.fetchall()

    db.cursor.execute("""
        SELECT championships.id
        FROM sessions
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE sessions.id = %s;""", (session_id,))
    championship = db.cursor.fetchone()

    db.cursor.execute("""
        SELECT driver_id
        FROM sessionsregistrations
        WHERE session_id = %s""", (session_id,))
    grid_size = db.cursor.fetchall()
    grid_size = len(grid_size)

    score_parameters = await get_score_parameters_of_a_championship(
        championship["id"],
        db=db,
        current_user=user
    )

    for prediction in predictions:
        new_potential = compute_score(
            user_driver_prediction=prediction["mygrid"],
            mygrid_driver_prediction=prediction["prediction"],
            driver_result=prediction["mygrid"],
            grid_size=grid_size,
            parameters=score_parameters
        )

        db.cursor.execute("""
            UPDATE sessionspredictions
            SET potential = %s
            WHERE session_id = %s
            AND user_id = %s
            AND driver_id = %s""", (new_potential, session_id, prediction["user_id"], prediction["driver_id"]))

    db.conn.commit()