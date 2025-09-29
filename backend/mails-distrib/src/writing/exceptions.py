from fastapi import HTTPException, status

from .texts import (
    no_fields_found_message,
    invalid_fields_message
)

class NoFieldsFound(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(**kwargs)
        self.detail = no_fields_found_message[language]

class InvalidFieldsException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(**kwargs)
        self.detail = invalid_fields_message[language]