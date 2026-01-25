import datetime

from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from psycopg.errors import UniqueViolation

from jose import jwt
from starlette.responses import Response

from backend import exceptions as app_exceptions
from backend.obligations import create_obligation

from backend.db.database import get_db, Database
from backend.config import settings as app_settings
from backend.utils import hash_password, verify, random_code
from backend.oauth2 import create_jwt_token, get_current_token, get_current_user, verify_refresh_token, \
    verify_access_token
from backend.src.auth import exceptions as auth_exceptions
from backend.src.auth import signals as auth_signals
from backend.src.auth.apple import validate_apple_token, verify_apple_id_token, get_user_id_from_apple_id
from backend.src.auth.google import verify_google_token, google_automatic_password, get_user_id_from_google_id
from backend.src.auth.referrals import assign_user_referral, create_unique_referral_code
from backend.src.auth.schemas import LoginResponse, AccessToken, LoginRefreshTokenPost
from backend.src.auth.security import get_login_cooldown_seconds, purge_user_login_attempts, generate_safe_username
from backend.src.auth.syntax import valid_username, valid_password, valid_email
from backend.src.users import signals as users_signals
from backend.src.users import exceptions as user_exceptions
from backend.src.users.privileges import is_user_banned
from backend.src.users.schemas import UserCreate, UserSelf
from backend.src.users.utils import get_user_id_from_email

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
        await valid_email(user.email, language=language)

        user.password = hash_password(user.password)

        # Create a unique code for referral purpose
        unique_referral_code = await create_unique_referral_code()

        # TODO: include add image at creation
        db.cursor.execute("""
            INSERT INTO users (username, email, password, language, referralcode)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *""", (user.username, user.email, user.password, language, unique_referral_code))
        new_user = db.cursor.fetchone()
        db.conn.commit()

        # TODO: add user in leaderboards

        # TODO include referral system
        if referral_code:
            await assign_user_referral(referral_code, new_user["id"], language=language)

        await users_signals.created.send(UserSelf(**new_user))

        # TODO: include full profile return
        return new_user

    except UniqueViolation as err:
        db.cursor.execute("ROLLBACK")
        db.conn.commit()
        raise app_exceptions.UnexpectedError(language=language)


@router.post("/login-email", response_model=LoginResponse)
async def login_email(request: Request, language: str = "en", db: Database = Depends(get_db),
          credentials: OAuth2PasswordRequestForm = Depends()):
    # TODO implement forgot password
    # TODO update Expo push token

    # Check if the ip address is in an incremental suspension
    cooldown_seconds = await get_login_cooldown_seconds(request.client.host)
    if cooldown_seconds > 0:
        raise auth_exceptions.LoginSuspendedError(cooldown_seconds, language=language)

    db.cursor.execute("""
        SELECT *
        FROM users
        WHERE email = %s
        OR username = %s""", (credentials.username, credentials.username))
    user = db.cursor.fetchone()

    if not user or not verify(credentials.password, user["password"]):
        #TODO Increment the loginattempt table
        raise auth_exceptions.WrongCredentialsError(language=language)
    else:
        await purge_user_login_attempts(user["id"], request.client.host)

    # Block banned users
    if await is_user_banned(user["id"]):
        raise user_exceptions.BannedUserException(user_id=user["id"], language=language)

    access_token = await create_jwt_token({
        "user_id": user["id"],
        "username": user["username"],
        "language": language
    })

    refresh_token = await create_jwt_token({
        "user_id": user["id"],
        "makeunique": random_code(32)
    }, datetime.timedelta(minutes=app_settings.refresh_token_expires_minutes))

    # Register the refresh token in the database to
    # be able to revoke it when logging out
    db.cursor.execute("""\
        INSERT INTO refreshtokens (user_id, token)
        VALUES (%s, %s)""", (user["id"], refresh_token))
    db.conn.commit()

    # TODO : return full profile

    return {
        "access_token": {
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
async def login_refresh_token(request: Request, tokens: LoginRefreshTokenPost, language: str = "en", db: Database = Depends(get_db)):

    # Check if the ip address is in an incremental suspension
    cooldown_seconds = await get_login_cooldown_seconds(request.client.host)
    if cooldown_seconds > 0:
        raise auth_exceptions.LoginSuspendedError(cooldown_seconds, language=language)

    refresh_token_data = await verify_refresh_token(tokens.refresh_token.refresh_token, language=language)
    token_data = await verify_access_token(tokens.access_token.access_token, language=language, verify_exp=False)

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
    if await is_user_banned(user["id"]):
        raise user_exceptions.BannedUserException(user_id=user["id"], language=language)

    # Revoke current token
    db.cursor.execute("""
        INSERT INTO revokedtokens (token)
        VALUES (%s)
        RETURNING *
        """, (tokens.access_token.access_token,))
    db.conn.commit()

    access_token = await create_jwt_token({
        "username": user["username"],
        "language": language
    })

    return {
        "access_token": {
            "access_token": access_token,
            "token_type": "bearer"
        },
        "user": user
    }


@router.post("/login-google", response_model=LoginResponse, status_code= status.HTTP_202_ACCEPTED)
async def login_google(credential: str, referral_code: str = None, language: str = "en", db: Database = Depends(get_db)):
    datas = await verify_google_token(credential, language=language)

    # Check if user has its email in the database
    user_id = await get_user_id_from_email(datas.email)

    # Check if a user is already assigned to this google_id
    has_google_id = await get_user_id_from_google_id(datas.sub) is not None

    # Check if the email has a @gmail.com suffix
    # We trust the user by skipping password verification if his mail is a @gmail.com
    # Google is authoritative if email has a @gmail.com suffix.
    is_google_email = datas.email.endswith("@gmail.com")

    # Google is authoritative if this is a professional Google paid service (Google Workspace) email
    # 'hd' claim is not absent if this is a Google Workspace email
    if not is_google_email:
        is_google_email = datas.hd is not None

    # Block banned users
    if user_id:
        if await is_user_banned(user_id):
            raise user_exceptions.BannedUserException(user_id=user_id, language=language)

    # Manage a registered user that doesn't have a google id associated yet
    if user_id and not has_google_id:
        # Associate our user's MyGrid database id to the given Google id
        try:
            db.cursor.execute("""\
                INSERT INTO googleids (user_id, google_id)
                VALUES (%s, %s)""", (user_id, datas.sub))
            db.conn.commit()

        except UniqueViolation as err:
            db.cursor.execute("ROLLBACK")
            db.conn.commit()
            raise app_exceptions.UnexpectedError(language=language)

        # Return the LoginResponse schema : access_token, refresh_token and user datas
        db.cursor.execute("""\
            SELECT * FROM users
            WHERE id = %s""", (user_id,))
        user = db.cursor.fetchone()

        access_token = await create_jwt_token({
            "user_id": user["id"],
            "username": user["username"],
            "language": language
        })

        refresh_token = await create_jwt_token({
            "user_id": user["id"],
            "makeunique": random_code(32)
        }, datetime.timedelta(minutes=app_settings.refresh_token_expires_minutes))

        return {
            "access_token": {
                "access_token": access_token,
                "token_type": "bearer"
            },
            "refresh_token": {
                "refresh_token": refresh_token,
                "token_type": "bearer"
            },
            "user": user
        }


    # Manage a registered user
    if user_id and has_google_id:
        # Return the LoginResponse schema : access_token, refresh_token and user datas
        db.cursor.execute("""\
            SELECT * FROM users
            WHERE id = %s""", (user_id,))
        user = db.cursor.fetchone()

        access_token = await create_jwt_token({
            "user_id": user["id"],
            "username": user["username"],
            "language": language
        })

        refresh_token = await create_jwt_token({
            "user_id": user["id"],
            "makeunique": random_code(32)
        })

        return {
            "access_token": {
                "access_token": access_token,
                "token_type": "bearer"
            },
            "refresh_token": {
                "refresh_token": refresh_token,
                "token_type": "bearer"
            },
            "user": user
        }

    # In none of the conditions above matched, we assume user_id is None

    # Manage an unregistered user by creating a new user and associate its id to google id

    # Trust @gmail.com emails by skipping the password creation
    # Else, create a temporary password that will be used
    # to request new credentials while assuring the user identity.
    if is_google_email:
        password = hash_password(await google_automatic_password(datas.sub))
    else:
        password = random_code(64)

    # Create a unique code for referral purpose
    unique_referral_code = await create_unique_referral_code()

    try:
        db.cursor.execute("""
            INSERT INTO users (username, email, password, language, referralcode, verified)
            VALUES (%s, %s, %s, %s, %s, true)
            RETURNING *""", (await generate_safe_username(), datas.email, password, language, unique_referral_code))
        new_user = db.cursor.fetchone()
        db.conn.commit()

    except UniqueViolation as err:
        db.cursor.execute("ROLLBACK")
        db.conn.commit()
        raise app_exceptions.UnexpectedError(language=language)

    if referral_code:
        await assign_user_referral(referral_code, new_user["id"], language=language)

    # Associate our user's MyGrid database id to the given Google id
    try:
        db.cursor.execute("""
            INSERT INTO googleids (user_id, google_id)
            VALUES (%s, %s)""", (new_user["id"], datas.sub))
        db.conn.commit()

    except UniqueViolation as err:
        db.cursor.execute("ROLLBACK")
        db.conn.commit()
        raise app_exceptions.UnexpectedError(language=language)

    # Create a new username and, if not a google_email, a new password
    await create_obligation(code= "newname", user_id= new_user["id"], language= language)
    if not is_google_email:
        await create_obligation(code= "newpwd", user_id= new_user["id"], language= language)

    return Response(status_code= status.HTTP_202_ACCEPTED)


@router.post("/login-apple", response_model=LoginResponse, status_code= status.HTTP_202_ACCEPTED)
async def login_apple(credential: str, nonce: str, referral_code: str = None, language: str = "en", db: Database = Depends(get_db)):
    datas = await validate_apple_token(authorization_code= credential, language=language)

    id_token = datas["id_token"]
    # access_token = datas["access_token"]
    # refresh_token = datas["refresh_token"]

    id_token_datas = await verify_apple_id_token(id_token, nonce= nonce)

    # Check if user has its email in the database
    if id_token_datas.email:
        user_id = await get_user_id_from_email(id_token_datas.email)
        email = id_token_datas.email
    else:
        user_id = None
        email = "apple@nomail.com"

    # Block banned users
    if user_id:
        if await is_user_banned(user_id):
            raise user_exceptions.BannedUserException(user_id=user_id, language=language)

    # Check if a user is already assigned to this apple_id
    has_apple_id = await get_user_id_from_apple_id(id_token_datas.sub) is not None

    # Manage a registered user that doesn't have an apple id associated yet
    if user_id and not has_apple_id:
        # Associate our user's MyGrid database id to the given Google id
        try:
            db.cursor.execute("""\
                INSERT INTO appleids (user_id, apple_id)
                VALUES (%s, %s)""", (user_id, id_token_datas.sub))
            db.conn.commit()

        except UniqueViolation as err:
            db.cursor.execute("ROLLBACK")
            db.conn.commit()
            raise app_exceptions.UnexpectedError(language=language)

        # Return the LoginResponse schema : access_token, refresh_token and user datas
        db.cursor.execute("""\
            SELECT * FROM users
            WHERE id = %s""", (user_id,))
        user = db.cursor.fetchone()

        access_token = await create_jwt_token({
            "user_id": user["id"],
            "username": user["username"],
            "language": language
        })

        refresh_token = await create_jwt_token({
            "user_id": user["id"],
            "makeunique": random_code(32)
        }, datetime.timedelta(minutes=app_settings.refresh_token_expires_minutes))

        return {
            "access_token": {
                "access_token": access_token,
                "token_type": "bearer"
            },
            "refresh_token": {
                "refresh_token": refresh_token,
                "token_type": "bearer"
            },
            "user": user
        }


    # Manage a registered user
    if user_id and has_apple_id:
        # Return the LoginResponse schema : access_token, refresh_token and user datas
        db.cursor.execute("""\
            SELECT * FROM users
            WHERE id = %s""", (user_id,))
        user = db.cursor.fetchone()

        access_token = await create_jwt_token({
            "user_id": user["id"],
            "username": user["username"],
            "language": language
        })

        refresh_token = await create_jwt_token({
            "user_id": user["id"],
            "makeunique": random_code(32)
        })

        return {
            "access_token": {
                "access_token": access_token,
                "token_type": "bearer"
            },
            "refresh_token": {
                "refresh_token": refresh_token,
                "token_type": "bearer"
            },
            "user": user
        }

    # In none of the conditions above matched, we assume user_id is None

    # Manage an unregistered user by creating a new user and associate its id to apple id

    # Trust @gmail.com emails by skipping the password creation
    password = random_code(64)

    # Create a unique code for referral purpose
    unique_referral_code = await create_unique_referral_code()

    try:
        db.cursor.execute("""
            INSERT INTO users (username, email, password, language, referralcode, verified)
            VALUES (%s, %s, %s, %s, %s, true)
            RETURNING *""", (await generate_safe_username(), email, password, language, unique_referral_code))
        new_user = db.cursor.fetchone()
        db.conn.commit()

    except UniqueViolation as err:
        db.cursor.execute("ROLLBACK")
        db.conn.commit()
        raise app_exceptions.UnexpectedError(language=language)

    if referral_code:
        await assign_user_referral(referral_code, new_user["id"], language=language)

    # Associate our user's MyGrid database id to the given Google id
    try:
        db.cursor.execute("""
            INSERT INTO appleids (user_id, apple_id)
            VALUES (%s, %s)""", (new_user["id"], id_token_datas.sub))
        db.conn.commit()

    except UniqueViolation as err:
        db.cursor.execute("ROLLBACK")
        db.conn.commit()
        raise app_exceptions.UnexpectedError(language=language)

    # Create a new username and, if not a google_email, a new password
    await create_obligation(code= "newname", user_id= new_user["id"], language= language)

    return Response(status_code= status.HTTP_202_ACCEPTED)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user), current_token: AccessToken = Depends(get_current_token)):
    db.cursor.execute("""
        DELETE
        FROM refreshtokens
        WHERE user_id = %s
        RETURNING *""", (current_user.id,))
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


@router.post("/confirm-email", status_code=status.HTTP_202_ACCEPTED, response_class=RedirectResponse)
async def confirm_email(token: AccessToken, db: Database = Depends(get_db)):
    # A very exceptional occasion where the token is read
    # without validation to extract the user language
    token_payload = jwt.decode(token.access_token, app_settings.secret_key, app_settings.algorithm, options={"verify_signature": False})
    language = token_payload.get("language", "en")

    datas = await verify_access_token(token.access_token, language=language, verify_exp=False)

    try:
        db.cursor.execute("""
            UPDATE users
            SET verified = true
            WHERE username = %s AND email = %s
            RETURNING *
            """, (datas.username, datas.email))
        db.conn.commit()

        user = db.cursor.fetchone()

        await auth_signals.validate_mail.send(UserSelf(**user))

        return RedirectResponse(app_settings.confirmed_email_url)
    except:
        db.cursor.execute("ROLLBACK")
        db.conn.commit()

    raise app_exceptions.ForbiddenAccessException(language=language)
