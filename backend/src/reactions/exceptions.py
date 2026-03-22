from fastapi import HTTPException, status
from jinja2 import Environment

from backend.src.reactions.texts import *

class ReactionIsNotAnEmojiError(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    def __init__(self, reaction: str, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        jinja_template = Environment().from_string(reaction_is_not_an_emoji_message[language])
        self.detail = jinja_template.render(reaction=reaction)