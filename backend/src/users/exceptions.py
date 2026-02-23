from fastapi import HTTPException, status

from backend.db.database import get_db
from backend.src.users.texts import *


class FailedAuthorizationError(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    headers = {"WWW-Authenticate": "Bearer"}
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = failed_authorization_message[language]

class SessionExpiredError(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    headers = {"WWW-Authenticate": "Bearer"}
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = expired_session_message[language]

class NotAUserError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = not_a_user_message[language]

class BannedUserException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    headers = {"WWW-Authenticate": "Bearer"}
    def __init__(self, user_id: int, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        db = get_db()

        db.cursor.execute(""" \
            SELECT reason
            FROM bannedhistory
            WHERE user_id = %s
            ORDER BY created DESC""", (user_id,))
        last_user_ban_record = db.cursor.fetchone()

        if last_user_ban_record:
            self.detail = banned_user_message[language]+last_user_ban_record["reason"]
        else:
            self.detail = banned_user_message[language]

class NoUserFoundError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    headers = {"WWW-Authenticate": "Bearer"}
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = no_user_found_message[language]

class CannotUpdateUsernameError(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    headers = {"WWW-Authenticate": "Bearer"}
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = cannot_update_username_message[language]