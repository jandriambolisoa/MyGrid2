from datetime import datetime, timedelta, UTC

from backend.db.database import get_db
from backend.config import settings as app_settings
from backend.src.auth.constants import LOGIN_SUSPENSION_DURATION, INCREMENTAL_SUSPENSION_DURATIONS

async def get_login_cooldown_seconds(address) -> int:
    if app_settings.debug:
        return -1

    # Get a delta time from now and set this as the furthest
    # moment in time to look for login attempts
    look_from = datetime.now(UTC) - timedelta(seconds=LOGIN_SUSPENSION_DURATION)

    db = get_db()
    db.cursor.execute("""\
        SELECT *
        FROM loginattempts
        WHERE address = %s AND created > %s
        ORDER BY created DESC""", (address, look_from))
    attempts = db.cursor.fetchall()

    if attempts:
        suspension = INCREMENTAL_SUSPENSION_DURATIONS[len(attempts) - 1]
        # Get the next_attempt authorized time value and compare it to now.
        next_attempt = attempts[0]["created"] + timedelta(seconds=suspension)

        if not next_attempt < datetime.now(UTC):
            return round(next_attempt - datetime.now(UTC))

    return -1

async def purge_user_login_attempts(user_id: int) -> None:
    db = get_db()
    db.cursor.execute("""\
        DELETE FROM loginattempts
        WHERE address = %s""", (address,))
    db.conn.commit()

async def purge_user_refresh_tokens(user_id: int) -> None:
    db = get_db()
    db.cursor.execute("""\
        DELETE FROM refreshtokens
        WHERE user_id = %s""", (user_id,))
    db.conn.commit()

async def generate_safe_username(user_id: int = None) -> str:
    new_username = "user%09d" % user_id if user_id else None

    if not user_id:
        db = get_db()
        db.cursor.execute("""\
            SELECT username FROM users""")
        existing_usernames = db.cursor.fetchall()
        tmp_id = 999999999
        new_username = "user%09d" % tmp_id
        while new_username in existing_usernames:
            tmp_id = tmp_id -1
            new_username = "user%09d" % tmp_id

    return new_username
