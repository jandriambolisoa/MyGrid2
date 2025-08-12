from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from jose import jwt, exceptions

from backend.src.appstatus import exceptions as app_exceptions
from backend.db.database import Database, get_db
from backend.src.appstatus.server import is_server_on_maintenance
from backend.src.users import exceptions as user_exceptions
from backend.src.users.config import settings as user_settings
from backend.src.users.schemas import TokenData, UserSelf
from backend.src.users.privileges import is_user_banned

oauth2_scheme = OAuth2PasswordBearer("login")

def verify_access_token(token: str, language: str = 'en'):
    db = get_db()

    db.cursor.execute("""\
        SELECT *
        FROM revokedtokens
        WHERE token = %s""", (token,))
    if db.cursor.fetchone():
        raise user_exceptions.FailedAuthorizationError(language=language)

    try:
        payload = jwt.decode(token, user_settings.secret_key, user_settings.algorithm)
        username = payload.get("username")
        language = payload.get("language")
        if not username:
            raise user_exceptions.FailedAuthorizationError(language=language)

        return TokenData(
            username=username,
            language=language
        )

    except exceptions.ExpiredSignatureError:
        raise user_exceptions.SessionExpiredError(language=language)


def get_current_user(token: str = Depends(oauth2_scheme), db: Database = Depends(get_db)):
    """
    This depedency function gets the current user from the token. It will check in this order:
    If the token is valid, if the user exists, if the server is not on maintenance and if the
    user is not banned.
    :param token: The token in headers request
    :param db: The database
    :return: UserSelf pydantic model
    """
    token_data = verify_access_token(token)

    # Return current user datas
    db.cursor.execute("""\
        SELECT *
        FROM users
        WHERE username = %s""", (token_data.username,))
    current_user = db.cursor.fetchone()

    if not current_user:
        raise user_exceptions.FailedAuthorizationError(language=token_data.language)

    # Block request when server is on maintenance
    if is_server_on_maintenance():
        raise app_exceptions.MaintenanceServerError(language=token_data.language)

    # Block banned users
    if is_user_banned(token_data.user_id):

        db.cursor.execute("""\
            SELECT reason
            FROM bannedhistory
            WHERE user_id = %s
            ORDER BY created DESC""", (token_data.user_id,))
        last_user_ban_record = db.cursor.fetchone()

        raise user_exceptions.BannedUserException(reason=last_user_ban_record["reason"], language=token_data.language)

    current_user = UserSelf(
        **current_user
    )

    #TODO Block users who are not visible in the Online Manager

    return current_user
