from fastapi import HTTPException, status
from jinja2 import Environment

from backend.src.auth.texts import not_a_valid_username_length_message, not_a_valid_username_characters_message, \
    not_available_username_message, not_a_valid_password_length_message, not_a_valid_password_strength_message, \
    not_available_email_message, login_suspended_message, wrong_credentials_message

class NotAValidUsernameLengthError(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(**kwargs)
        self.detail = not_a_valid_username_length_message[language]

class NotAValidUsernameCharactersError(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(**kwargs)
        self.detail = not_a_valid_username_characters_message[language]

class NotAvailableUsernameError(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(**kwargs)
        self.detail = not_available_username_message[language]

class NotAValidPasswordLength(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(**kwargs)
        self.detail = not_a_valid_password_length_message[language]

class NotAValidPasswordStrength(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(**kwargs)
        self.detail = not_a_valid_password_strength_message[language]

class NotAvailableEmailError(HTTPException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(**kwargs)
        self.detail = not_available_email_message[language]

class LoginSuspendedError(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    def __init__(self, duration: int, language: str = "en", **kwargs):
        super().__init__(**kwargs)
        jinja_env = Environment(loader= login_suspended_message[language]) # TODO Check Jinja code
        self.detail = jinja_env.render(duration=duration)

class WrongCredentialsError(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    def __init__(self, language: str = "en", **kwargs):
        super().__init__(**kwargs)
        self.detail = wrong_credentials_message[language]
