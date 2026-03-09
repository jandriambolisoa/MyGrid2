from fastapi import HTTPException, status
from jinja2 import Environment

from backend.src.predictions.texts import *

class DriverNotRegisteredForSessionError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = driver_not_registered_for_session_message[language]

class PredictionNotAvailableError(HTTPException):
    status_code = status.HTTP_425_TOO_EARLY
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = prediction_not_available_message[language]

class NoPredictionError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = no_prediction_message[language]
