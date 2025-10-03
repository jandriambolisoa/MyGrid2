from fastapi import HTTPException, status

from backend.texts import *

class UnexpectedError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str, **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = unexpected_message[language]

class ForbiddenAccessException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    def __init__(self, language: str, **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = forbidden_access_message[language]
