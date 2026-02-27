from fastapi import HTTPException, status
from jinja2 import Environment

from backend.src.results.texts import *

class NoResultsFoundError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = no_results_found_message[language]

class InvalidSessionResultsAttemptError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = invalid_session_result_attempt_message[language]

class IncorrectNumberOfDriverError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = incorrect_number_of_driver_message[language]