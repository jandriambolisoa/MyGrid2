from fastapi import HTTPException, status
from jinja2 import Environment

from backend.src.drivers.texts import *

class NotAValidCodenameLengthError(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = not_a_valid_codename_length_message[language]

class NotAValidColorError(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = not_a_valid_color_message[language]

class DriverNotFoundError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = driver_not_found_message[language]

class DriverDoesNotExistsError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, driver_id: int = None, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        if not driver_id:
            self.detail = driver_not_found_message[language]
        jinja_template = Environment().from_string(driver_does_not_exists_message[language])
        self.detail = jinja_template.render(driver_id=driver_id)

class TeamDoesNotExistsError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, team_id: int = None, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        if not team_id:
            self.detail = team_not_found_message[language]
        jinja_template = Environment().from_string(team_does_not_exists_message[language])
        self.detail = jinja_template.render(team_id=team_id)

class TeamNotFoundError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = team_not_found_message[language]

class DriverAlreadyExistsError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = driver_already_exists_message[language]

class TeamAlreadyExistsError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = team_already_exists_message[language]

