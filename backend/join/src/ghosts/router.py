from datetime import datetime, UTC, timedelta

from fastapi import APIRouter, Depends
from psycopg.errors import UniqueViolation
from starlette import status

from backend.db.database import get_db, Database
from backend.join.src.ghosts.constants import GHOST_USER_EXPIRATION_HOURS
from backend.join.src.ghosts.schemas import GhostUserCreate
from backend.oauth2 import create_jwt_token
from backend.src.appstatus.server import get_latest_appstatus
from backend.src.auth.referrals import create_unique_referral_code, assign_user_referral
from backend.src.auth.schemas import LoginResponse
from backend.src.auth.syntax import valid_username
from backend.src.leagues.dependencies import valid_league_id
from backend.src.users import signals as users_signals
from backend.config import settings as app_settings
from backend.utils import random_code

router = APIRouter(
    prefix="/ghosts",
    tags= ["ghosts"]
)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=LoginResponse)
async def signup_ghost_user(
        user: GhostUserCreate,
        league_id: int = Depends(valid_league_id),
        language: str = "en",
        db: Database = Depends(get_db)):
    # Check credentials
    await valid_username(user.username, language=language)

    # Create a unique code for referral purpose
    unique_referral_code = await create_unique_referral_code()

    # TODO: include add image at creation

    # Create the user
    db.cursor.execute("""
        INSERT INTO users (username, language, referralcode)
        VALUES (%s, %s, %s)
        RETURNING *""", (user.username, language, unique_referral_code))
    new_user = db.cursor.fetchone()
    db.conn.commit()

    # Declare this user a ghost user
    db.cursor.execute("""
        INSERT INTO ghostusers (user_id, exp)
        VALUES (%s, %s)""", (new_user["id"], datetime.now(UTC)+timedelta(hours=GHOST_USER_EXPIRATION_HOURS)))
    db.conn.commit()

    # Assign the league's organizer as the referral of this ghost user
    db.cursor.execute("""
        SELECT users.referralcode 
        FROM leaguesusers
        LEFT JOIN users ON users.id = leaguesusers.id
        WHERE leaguesusers.league_id = %s
        AND leaguesusers.organizer = true""", (league_id,))
    organizer = db.cursor.fetchone()

    await assign_user_referral(organizer["referral_code"], new_user["id"], language=language)

    await users_signals.created.send(new_user["id"])

    access_token = await create_jwt_token({
        "user_id": new_user["id"],
        "username": new_user["username"],
        "language": language
    })

    refresh_token = await create_jwt_token({
        "user_id": new_user["id"],
        "makeunique": random_code(32)
    }, timedelta(minutes=app_settings.refresh_token_expires_minutes))

    # Register the refresh token in the database to
    # be able to revoke it when logging out
    db.cursor.execute("""\
        INSERT INTO refreshtokens (user_id, token)
        VALUES (%s, %s)""", (new_user["id"], refresh_token))
    db.conn.commit()

    return {
        "app_status": await get_latest_appstatus(),
        "access_token": {
            "access_token": access_token,
            "token_type": "bearer"
        },
        "refresh_token": {
            "refresh_token": refresh_token,
            "token_type": "bearer"
        },
        "user": new_user
    }
