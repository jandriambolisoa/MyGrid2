from backend.db.database import get_db
from backend.src.users import exceptions as user_exceptions

async def is_user_banned(user_id: int) -> bool:
    db = get_db()

    db.cursor.execute("""\
        SELECT banned
        FROM bannedhistory
        WHERE user_id = %s
        ORDER BY created DESC""", (user_id,))
    user_last_ban_record = db.cursor.fetchone()

    if not user_last_ban_record:
        return False
    elif user_last_ban_record["banned"]:
        return True
    else:
        return False

async def is_user_verified(user_id: int) -> bool:
    # Ignore privilege if the user is banned
    if await is_user_banned(user_id):
        return False

    db = get_db()

    db.cursor.execute("""\
        SELECT verified
        FROM users
        WHERE user_id = %s""", (user_id,))
    user = db.cursor.fetchone()

    if not user:
        raise user_exceptions.NotAUserError()

    if user["verified"]:
        return True
    else:
        return False

async def is_user_moderator(user_id: int) -> bool:
    # Ignore privilege if the user is banned
    if await is_user_banned(user_id):
        return False

    db = get_db()

    db.cursor.execute("""\
        SELECT moderator
        FROM promotedhistory
        WHERE user_id = %s
        ORDER BY created DESC""", (user_id,))
    user_last_promotion_record = db.cursor.fetchone()

    if not user_last_promotion_record:
        return False
    elif user_last_promotion_record["moderator"]:
        return True
    else:
        return False

async def is_user_admin(user_id: int) -> bool:
    # Ignore privilege if the user is banned
    if await is_user_banned(user_id):
        return False

    db = get_db()

    db.cursor.execute("""\
        SELECT admin
        FROM promotedhistory
        WHERE user_id = %s
        ORDER BY created DESC""", (user_id,))
    user_last_promotion_record = db.cursor.fetchone()

    if not user_last_promotion_record:
        return False
    elif user_last_promotion_record["moderator"]:
        return True
    else:
        return False

async def is_user_moderator_or_admin(user_id: int) -> bool:
    # Ignore privilege if the user is banned
    if await is_user_banned(user_id):
        return False

    db = get_db()

    db.cursor.execute("""\
        SELECT admin, moderator
        FROM promotedhistory
        WHERE user_id = %s
        ORDER BY created DESC""", (user_id,))
    user_last_promotion_record = db.cursor.fetchone()

    if not user_last_promotion_record:
        return False
    elif any([user_last_promotion_record["moderator"], user_last_promotion_record["admin"]]):
        return True
    else:
        return False
