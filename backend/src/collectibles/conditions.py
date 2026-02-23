from typing import List

from backend.db.database import get_db
from backend.src.events.dependencies import is_session_over
from backend.src.users.schemas import User

# Conditions in the collectible context list users that match given conditions.
# Those are used for distributing collectibles

async def multiple_drivers_perfect_prediction(session_id: int, drivers_id: List[int]) -> List[User]:
    valid_session = await is_session_over(session_id)

    if not valid_session:
        return []

    db = get_db()
    db.cursor.execute("""\
        WITH perfect_predictions AS (
            SELECT sessionspredictions.user_id,
            sessionspredictions.driver_id,
            sessionspredictions.mygrid,
            sessionsresults.result,
            COUNT(*) OVER (PARTITION BY user_id) AS nb_perfect_predictions
            FROM sessionspredictions
            LEFT JOIN sessionsresults ON sessionspredictions.session_id = sessionsresults.session_id
            AND sessionspredictions.driver_id = sessionsresults.driver_id
            WHERE sessionspredictions.session_id = %s
            AND sessionspredictions.driver_id = ANY(%s) 
            AND sessionspredictions.mygrid = sessionsresults.result
        )
        SELECT users.id,
        users.username,
        users.created,
        users.image
        FROM perfect_predictions
        LEFT JOIN users ON users.id = perfect_predictions.user_id
        WHERE perfect_predictions.nb_perfect_predictions = %s
        GROUP BY users.id, users.username, users.created, users.image""", (session_id, drivers_id, len(drivers_id)))
    users = db.cursor.fetchall()

    return [User(**user) for user in users]