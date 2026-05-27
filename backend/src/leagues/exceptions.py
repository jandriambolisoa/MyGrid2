from fastapi import HTTPException, status
from jinja2 import Environment

from backend.src.leagues.texts import *

class NoLeagueFoundError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = no_league_found_message[language]

class LeagueDoesNotExistsError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, league_id: int = None, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        if not league_id:
            self.detail = no_league_found_message[language]
        jinja_template = Environment().from_string(league_does_not_exists_message[language])
        self.detail = jinja_template.render(league_id=league_id)

class LeagueNotOwnedError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, league_id: int = None, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        if not league_id:
            self.detail = no_league_found_message[language]
        jinja_template = Environment().from_string(league_not_owned_message[language])
        self.detail = jinja_template.render(league_id=league_id)

class MaxLeagueCreationError(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = max_league_creation_message[language]

class NotAValidLeagueNameLengthError(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = not_a_valid_league_name_length_message[language]

class NotAValidLeagueNameCharactersError(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = not_a_valid_league_name_characters_message[language]

class NotAvailableLeagueNameError(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = not_available_league_name_message[language]

class LeagueAlreadyExistsError(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = league_already_exists_message[language]
