from fastapi import HTTPException, status

from backend.openf1.texts import (
    openf1_cannot_get_access_token,
    openf1_connection_failed_message
)

class OpenF1CannotGetAccessTokenException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = openf1_cannot_get_access_token[language]

class OpenF1ConnectionFailed(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = openf1_connection_failed_message[language]