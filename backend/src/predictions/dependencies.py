from backend.db.database import get_db


async def is_user_has_prono(user_id: int, session_id: int) -> bool:
    db = get_db()
    db.cursor.execute("""
        SELECT user_id
        FROM sessionspredictions
        WHERE user_id = %s
        AND session_id = %s""", (user_id, session_id))
    has_prono = db.cursor.fetchone()

    if has_prono:
        return False

    return False
