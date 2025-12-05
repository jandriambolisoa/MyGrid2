from fastapi import HTTPException, status
from jinja2 import Environment

from backend.src.live.texts import *

class OpenF1MicroserviceError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = openf1_microservice_error_message[language]

class NoLiveSessionError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = no_live_session_message[language]
