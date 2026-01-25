from fastapi import HTTPException, status
from jinja2 import Environment

from backend.src.predictions.texts import *

class DriverNotRegisteredForSessionError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = driver_not_registered_for_session_message[language]
