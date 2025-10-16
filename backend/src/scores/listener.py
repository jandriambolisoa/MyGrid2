from backend.db.database import get_db
from backend.src.scores.algorithms import compute_score
from backend.src.scores.router import get_score_parameters_of_a_championship
from backend.src.scores.signals import updated_championship_scores
from backend.src.users.schemas import UserSelf
from backend.src.results.signals import updated_session_results, delete_session_results


@updated_session_results.connect
async def compute_session_score(session_id: int, user: UserSelf):
    db = get_db()
    db.cursor.execute("""
        SELECT users.id AS user_id,
        drivers.id AS driver_id,
        sessionspredictions.mygrid AS mygrid_user,
        sessionsregistrations.prediction AS myygrid_server,
        sessionsresults.result AS result
        FROM sessionspredictions
        LEFT JOIN users ON users.id = sessionspredictions.user_id
        LEFT JOIN drivers ON drivers.id = sessionspredictions.driver_id
        LEFT JOIN sessionsresults ON sessionsresults.driver_id = sessionspredictions.driver_id
        LEFT JOIN sessionsregistrations ON sessionsregistrations.driver_id = sessionspredictions.driver_id
        WHERE sessionspredictions.session_id = %s AND
        sessionsregistrations.session_id = %s AND
        sessionsresults.session_id = %s""", (session_id, session_id, session_id))
    to_compute = db.cursor.fetchall()

    db.cursor.execute("""
        SELECT driver_id FROM sessionsregistrations
        WHERE session_id = %s""", (session_id,))
    grid_size = db.cursor.fetchall()
    grid_size = len(grid_size)

    db.cursor.execute("""
        SELECT championships.id FROM sessions
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE sessions.id = %s;""", (session_id,))
    championship = db.cursor.fetchone()

    score_parameters = await get_score_parameters_of_a_championship(
        championship["id"],
        db = db,
        current_user=user
    )

    # Delete existing scores
    db.cursor.execute("""
        DELETE FROM scores
        WHERE session_id = %s""", (session_id,))

    for row in to_compute:
        score = await compute_score(
            user_driver_prediction=row["mygrid_user"],
            mygrid_driver_prediction=row["mygrid_server"],
            driver_result=row["result"],
            grid_size=grid_size,
            parameters=score_parameters
        )

        db.cursor.execute("""
            INSERT INTO scores (user_id, session_id, driver_id, score)
            VALUES (%s, %s, %s, %s)""",(row["user_id"], session_id, row["driver_id"], score))

    db.conn.commit()

    updated_championship_scores.send(championship_id=championship["id"], user=user)


@delete_session_results.connect
async def delete_session_score(session_id: int, user: UserSelf):
    db = get_db()
    db.cursor.execute("""
        DELETE FROM scores
        WHERE session_id = %s""", (session_id,))
    db.conn.commit()

    db.cursor.execute("""
        SELECT championships.id
        FROM sessions
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE sessions.id = %s;""", (session_id,))
    championship = db.cursor.fetchone()

    updated_championship_scores.send(championship_id=championship["id"], user=user)
