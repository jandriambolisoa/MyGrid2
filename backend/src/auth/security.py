from datetime import datetime, timedelta, UTC

from backend.db.database import get_db
from backend.config import settings as app_settings
from backend.src.auth.constants import LOGIN_SUSPENSION_DURATION, INCREMENTAL_SUSPENSION_DURATIONS

def get_login_cooldown_seconds(address) -> int:
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

def purge_user_login_attempts(address: str) -> None:
    db = get_db()
    db.cursor.execute("""\
        DELETE FROM loginattempts
        WHERE address = %s""", (address,))
    db.conn.commit()

def purge_user_refresh_tokens(address: str) -> None:
    db = get_db()
    db.cursor.execute("""\
        DELETE FROM refreshtokens
        WHERE address = %s""", (address,))
    db.conn.commit()