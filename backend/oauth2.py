from datetime import datetime, UTC, timedelta

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from jose import jwt, exceptions
from jose.exceptions import JWTError

from backend.src.appstatus import exceptions as app_exceptions
from backend.db.database import Database, get_db
from backend.src.appstatus.server import is_server_on_maintenance
from backend.src.users import exceptions as user_exceptions
from backend.config import settings as app_settings
from backend.src.users.schemas import UserSelf
from backend.src.auth.schemas import AccessTokenData, AccessToken, RefreshTokenData
from backend.src.users.privileges import is_user_banned

oauth2_scheme = OAuth2PasswordBearer("login")

async def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(minutes=app_settings.token_expires_minutes)):
    try:
        to_encode = data.copy()

        expire_datetime = datetime.now(UTC) + expires_delta
        to_encode["exp"] = expire_datetime

        encoded_jwt = jwt.encode(to_encode, app_settings.secret_key, app_settings.algorithm)
        return encoded_jwt

    except:
        raise JWTError()

async def verify_access_token(token: str, language: str = 'en', verify_exp: bool = True):
    if await is_token_revoked(token):
        raise user_exceptions.FailedAuthorizationError(language=language)

    try:
        payload = jwt.decode(token, app_settings.secret_key, app_settings.algorithm, options={"verify_exp": verify_exp})
        user_id = payload.get("user_id")
        username = payload.get("username")
        language = payload.get("language")
        if not username:
            raise user_exceptions.FailedAuthorizationError(language=language)

        return AccessTokenData(
            user_id=user_id,
            username=username,
            language=language
        )

    except exceptions.ExpiredSignatureError:
        raise user_exceptions.SessionExpiredError(language=language)

async def verify_refresh_token(token: str, language: str = 'en'):
    if await is_token_revoked(token):
        raise user_exceptions.FailedAuthorizationError(language=language)

    try:
        payload = jwt.decode(token, app_settings.secret_key, app_settings.algorithm)
        user_id = payload.get("user_id")
        if not user_id:
            raise user_exceptions.SessionExpiredError(language=language)

        return RefreshTokenData(
            user_id=user_id
        )

    except exceptions.ExpiredSignatureError:
            raise user_exceptions.SessionExpiredError(language=language)

async def revoke_token(token: str):
    db = get_db()
    db.cursor.execute("""\
        INSERT INTO revokedtokens (token)
        VALUES (%s)""", (token,))
    db.conn.commit()

async def is_token_revoked(token: str) -> bool:
    db = get_db()
    db.cursor.execute(""" \
        SELECT *
        FROM revokedtokens
        WHERE token = %s""", (token,))
    if db.cursor.fetchone():
        return True
    return False

async def get_current_user(token: str = Depends(oauth2_scheme), db: Database = Depends(get_db)):
    """
    This depedency function gets the current user from the token. It will check in this order:
    If the token is valid, if the user exists, if the server is not on maintenance and if the
    user is not banned.
    :param token: The token in headers request
    :param db: The database
    :return: UserSelf pydantic model
    """
    token_data = await verify_access_token(token)

    # Return current user datas
    db.cursor.execute("""\
        SELECT *
        FROM users
        WHERE username = %s""", (token_data.username,))
    current_user = db.cursor.fetchone()

    if not current_user:
        raise user_exceptions.FailedAuthorizationError(language=token_data.language)

    # Block request when server is on maintenance
    if await is_server_on_maintenance():
        raise app_exceptions.MaintenanceServerError(language=token_data.language)

    # Block banned users
    if await is_user_banned(token_data.user_id):
        raise user_exceptions.BannedUserException(user_id=token_data.user_id, language=token_data.language)

    current_user = UserSelf(
        **current_user
    )

    #TODO Block users who are not visible in the Online Manager

    return current_user

async def get_current_token(token: str = Depends(oauth2_scheme)):
    token_data = await verify_access_token(token)
    token = AccessToken(
        access_token=token,
        token_type="bearer"
    )
    return token