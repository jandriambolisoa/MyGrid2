from fastapi import HTTPException, status
from jinja2 import Environment

from backend.src.registrations.texts import *

class NoRegistrationsFoundError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = no_registrations_found_message[language]

class RegistrationAlreadyExistsError(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = registration_already_exists_message[language]

class RegistrationCannotSwapWithAlreadyRegisteredDriverError(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = registration_cannot_swap_with_already_registered_driver_message[language]


class InvalidSessionRegistrationAttemptError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = invalid_session_registration_attempt_message[language]