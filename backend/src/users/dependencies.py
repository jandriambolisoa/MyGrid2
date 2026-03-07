from fastapi import Depends

from backend.db.database import get_db, Database
from backend.oauth2 import get_current_user
from backend.src.users.exceptions import NotAUserError
from backend.src.users.privileges import is_user_banned
from backend.src.users.schemas import UserSelf


async def valid_user_id(user_id: int = None, current_user: UserSelf = Depends(get_current_user)) -> int or None:
    if not user_id:
        return None

    if await is_user_banned(user_id):
        raise NotAUserError(current_user.language)

    db = get_db()
    db.cursor.execute("""
        SELECT id FROM users
        WHERE id = %s""", (user_id,))
    user = db.cursor.fetchone()
    if not user:
        raise NotAUserError(current_user.language)

    return user_id

async def valid_user_username(username: str = None, current_user: UserSelf = Depends(get_current_user)) -> str or None:
    if not username:
        return None

    db = get_db()
    db.cursor.execute("""
        SELECT id, username FROM users
        WHERE username = %s""", (username,))
    user = db.cursor.fetchone()

    if not user:
        raise NotAUserError(current_user.language)

    if await is_user_banned(user["id"]):
        raise NotAUserError(current_user.language)

    return user["username"]

async def get_current_user_language(language: str = None, current_user: UserSelf = Depends(get_current_user)) -> str:
    if not language:
        return current_user.language
    else:
        db = get_db()
        db.cursor.execute("""
            UPDATE users
            SET language = %s
            WHERE id = %s""", (language, current_user.id))
        db.conn.commit()

        return language

async def is_user_have_obligation(user_id: int, obligation: str = None):
    db = get_db()
    if obligation:
        db.cursor.execute("""\
            SELECT *
            FROM userobligations
            WHERE user_id = %s AND obligation = %s""", (user_id, obligation))
        has_obligation = db.cursor.fetchone()
    else:
        db.cursor.execute("""\
            SELECT *
            FROM userobligations
            WHERE user_id = %s""", (user_id, obligation))
        has_obligation = db.cursor.fetchone()

    if has_obligation:
        return True

    return False