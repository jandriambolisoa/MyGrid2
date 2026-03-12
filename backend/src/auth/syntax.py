import string

from pydantic import EmailStr

from backend.db.database import get_db

from backend.src.users.schemas import UserCreate
from backend.src.auth.constants import USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH, PW_MIN_LENGTH
from backend.src.auth.exceptions import NotAValidUsernameLengthError, NotAValidUsernameCharactersError, \
    NotAvailableUsernameError, NotAValidPasswordLength, NotAValidPasswordStrength, NotAValidEmailError, \
    NotAValidUsernameSpacebarError


async def valid_username(username: str, language: str = "en") -> str:
    if len(username) > USERNAME_MAX_LENGTH or len(username) < USERNAME_MIN_LENGTH:
        raise NotAValidUsernameLengthError(language=language)

    authorized_characters = [*string.ascii_lowercase, *string.ascii_uppercase, *string.digits, "_", "-"]

    for character in username:
        if character == " ":
            raise NotAValidUsernameSpacebarError(language=language)
        if not character in authorized_characters:
            raise NotAValidUsernameCharactersError(language=language)

    db = get_db()

    db.cursor.execute("""
        SELECT bannedusernames.username
        FROM bannedusernames
        WHERE bannedusernames.username = %s
        UNION
        SELECT users.username
        FROM users
        WHERE users.username = %s""", (username, username))
    is_unavailable = db.cursor.fetchone()

    if is_unavailable:
        raise NotAvailableUsernameError(language=language)

    return username

async def valid_password(input: str, language: str = "en") -> str:
    if len(input) < PW_MIN_LENGTH:
        raise NotAValidPasswordLength(language=language)

    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False

    for char in input:

        if char.islower():
            has_lower = True

        if char.isupper():
            has_upper = True

        if char.isdigit():
            has_digit = True

        if not char.isalnum():
            has_special = True

    if [has_lower, has_upper, has_digit, has_special].count(False) > 1:
        raise NotAValidPasswordStrength(language=language)

    return input

async def valid_email(input: str, language: str = "en") -> str:
    if not "@" in input:
        raise NotAValidEmailError(language=language)

    email_elements = input.split("@")
    if len(email_elements[0]) == 0 or len(email_elements[1]) == 0:
        raise NotAValidEmailError(language=language)

    return input
