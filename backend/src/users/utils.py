from backend.db.database import get_db


async def get_user_id_from_email(email: str) -> int:
    db = get_db()
    db.cursor.execute("""\
        SELECT id FROM users
        WHERE email = %s""", (email,))
    user_id = db.cursor.fetchone()
    return user_id["id"] if user_id else None