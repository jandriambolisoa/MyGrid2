from fastapi import APIRouter, status, Depends, Request, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from psycopg.errors import UniqueViolation

from backend import exceptions as app_exceptions
from backend.src.auth import exceptions as auth_exceptions
from backend.src.users import exceptions as user_exceptions

from backend.oauth2 import create_jwt_token, get_current_token, get_current_user, verify_refresh_token, \
    verify_access_token
from backend.src.auth.schemas import LoginResponse, AccessToken, LoginRefreshTokenPost
from backend.src.users.privileges import is_user_banned
from backend.utils import hash, verify, random_code
from backend.src.auth.security import get_login_cooldown_seconds, purge_user_login_attempts
from backend.src.auth.syntax import valid_username, valid_password
from backend.src.auth.referrals import assign_user_referral, create_unique_referral_code
from backend.src.users.schemas import UserCreate, UserSelf
from backend.db.database import get_db, Database

router = APIRouter(
    prefix="/auth",
    tags= ["auth"]
)


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserSelf)
async def signup_user(user: UserCreate, referral_code: str = None, language: str = None, db: Database = Depends(get_db)):
    # Removed the server maintenance condition
    # We must worship a user initiative to sing-up and therefore
    # try our best to make it happen in any condition
    try:
        # Check credentials
        await valid_username(user.username, language=language)
        await valid_password(user.password, language=language)

        user.password = hash(user.password)

        # Create a unique code for referral purpose
        unique_referral_code = create_unique_referral_code()

        # TODO: include add image at creation
        db.cursor.execute("""
            INSERT INTO users (username, email, password, language, referralcode)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *""", (user.username, user.email, user.password, language, unique_referral_code))
        new_user = db.cursor.fetchone()
        db.conn.commit()

        # TODO: add user in leaderboards

        # TODO: include automatic email verification
        #_send_verification_mail(user.username, user.email)

        # TODO include referral system
        if referral_code:
            assign_user_referral(referral_code, new_user["id"], language=language)

        # TODO: include full profile return
        return new_user

    except UniqueViolation as err:
        db.cursor.execute("ROLLBACK")
        db.conn.commit()
        raise app_exceptions.UnexpectedError(language=language)


@router.post("/login-email", response_model=LoginResponse)
def login_email(request: Request, language: str = "en", db: Database = Depends(get_db),
          credentials: OAuth2PasswordRequestForm = Depends()):
    # TODO implement forgot password
    # TODO update Expo push token

    # Check if the ip address is in an incremental suspension
    cooldown_seconds = get_login_cooldown_seconds(request.client.host)
    if cooldown_seconds > 0:
        raise auth_exceptions.LoginSuspendedError(cooldown_seconds, language=language)

    db.cursor.execute("""
        SELECT *
        FROM users
        WHERE email = %s
        OR username = %s""", (credentials.username, credentials.username))
    user = db.cursor.fetchone()

    if not user or not verify(credentials.password, user["password"]):
        raise auth_exceptions.WrongCredentialsError(language=language)
    else:
        purge_user_login_attempts(user["id"])

    # Block banned users
    if is_user_banned(user["id"]):
        raise user_exceptions.BannedUserException(user_id=user["id"], language=language)

    access_token = create_jwt_token({
        "username": user["username"],
        "language": language
    })

    refresh_token = create_jwt_token({
        "user_id": user["id"],
        "makeunique": random_code(32)
    })

    # Register the refresh token in the database to
    # be able to revoke it when logging out
    db.cursor.execute("""\
        INSERT INTO refreshtokens (user_id, refresh_token)
        VALUES (%s, %s)""", (user["id"], refresh_token))
    db.conn.commit()

    # TODO : return full profile

    return {
        "token": {
            "access_token": access_token,
            "token_type": "bearer"
        },
        "refresh_token": {
            "refresh_token": refresh_token,
            "token_type": "bearer"
        },
        "user": user
    }


@router.post("/login-refresh-token", response_model=LoginResponse)
def login_refresh_token(request: Request, tokens: LoginRefreshTokenPost, language: str = "en", db: Database = Depends(get_db)):

    # Check if the ip address is in an incremental suspension
    cooldown_seconds = get_login_cooldown_seconds(request.client.host)
    if cooldown_seconds > 0:
        raise auth_exceptions.LoginSuspendedError(cooldown_seconds, language=language)

    refresh_token_data = verify_refresh_token(tokens.refresh_token.refresh_token, language=language)
    token_data = verify_access_token(tokens.access_token.access_token, language=language, verify_exp=False)

    # Return current user datas
    db.cursor.execute(""" \
        SELECT *
        FROM users
        WHERE username = %s""", (token_data.username,))
    user = db.cursor.fetchone()

    if not user:
        raise user_exceptions.FailedAuthorizationError(language=language)

    if not refresh_token_data.user_id == user["id"]:
        raise user_exceptions.FailedAuthorizationError(language=language)

    # Block banned users
    if is_user_banned(user["id"]):
        raise user_exceptions.BannedUserException(user_id=user["id"], language=language)

    # Revoke current token
    db.cursor.execute("""
        INSERT INTO revokedtokens (token)
        VALUES (%s)
        RETURNING *
        """, (tokens.access_token.access_token,))
    db.conn.commit()

    access_token = create_jwt_token({
        "username": user["username"],
        "language": language
    })

    return {
        "token": {
            "access_token": access_token,
            "token_type": "bearer"
        },
        "user": user
    }

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user), current_token: AccessToken = Depends(get_current_token)):
    db.cursor.execute("""
        SELECT *
        FROM refreshtokens
        WHERE user_id = %s;
        DELETE
        FROM refreshtokens
        WHERE user_id = %s;""", (current_user.id, current_user.id))
    refresh_tokens = db.cursor.fetchall()
    db.conn.commit()

    for refresh_token in refresh_tokens:
        db.cursor.execute("""
            INSERT INTO revokedtokens (token)
            VALUES (%s)""", (refresh_token["token"]))

    db.cursor.execute("""
        INSERT INTO revokedtokens (token)
        VALUES (%s)""", (current_token.access_token,))

    db.conn.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
