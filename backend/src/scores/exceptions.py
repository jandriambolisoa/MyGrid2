from fastapi import HTTPException, status
from jinja2 import Environment

from backend.src.scores.texts import *

class NoParametersFoundError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, championship_id: int, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = no_parameters_found_message[language] + str(championship_id)
