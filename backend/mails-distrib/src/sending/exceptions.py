from fastapi import HTTPException, status

from .texts import (
    email_authentification_message,
)

class EmailAuthenticationException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(**kwargs)
        self.detail = email_authentification_message[language]
