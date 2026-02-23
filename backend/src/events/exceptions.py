from fastapi import HTTPException, status
from jinja2 import Environment

from backend.src.events.texts import *

class ChampionshipAlreadyExistsError(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = championship_already_exists_message[language]

class EventAlreadyExistsError(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = event_already_exists_message[language]

class SessionAlreadyExistsError(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = session_already_exists_message[language]

class InvalidDatetimeStringError(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = invalid_datetime_string_message[language]

class InvalidDatetimeForSessionCreationError(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = invalid_datetime_for_session_creation_message[language]

class ChampionshipDoesNotExistsError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, championship_id: int = None, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        if not championship_id:
            self.detail = championship_not_found_message[language]
        jinja_template = Environment().from_string(championship_does_not_exists_message[language])
        self.detail = jinja_template.render(championship_id=championship_id)

class EventDoesNotExistsError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, event_id: int = None, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        if not event_id:
            self.detail = championship_not_found_message[language]
        jinja_template = Environment().from_string(event_does_not_exists_message[language])
        self.detail = jinja_template.render(event_id=event_id)

class SessionDoesNotExistsError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, session_id: int = None, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        if not session_id:
            self.detail = championship_not_found_message[language]
        jinja_template = Environment().from_string(session_does_not_exists_message[language])
        self.detail = jinja_template.render(session_id=session_id)

class ChampionshipNotFoundError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = championship_not_found_message[language]

class EventNotFoundError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = event_not_found_message[language]

class SessionNotFoundError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = session_not_found_message[language]

class SessionStartedError(HTTPException):
    status_code = status.HTTP_412_PRECONDITION_FAILED
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = session_started_message[language]

class TooLateToMakeAChampionshipPrediction(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = too_late_to_make_a_championship_prediction_message[language]