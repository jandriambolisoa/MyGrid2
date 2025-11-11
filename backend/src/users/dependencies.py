from fastapi import Depends

from backend.db.database import get_db
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
