from fastapi import HTTPException, status
from jinja2 import Environment

from backend.src.notifications.texts import not_a_valid_push_token_message
from backend.src.ranks.texts import *

class NotAValidPushTokenError(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = not_a_valid_push_token_message[language]
