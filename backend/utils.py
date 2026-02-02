import string
import random
import hashlib
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from datetime import datetime
from jinja2 import Environment

from backend.texts import days_of_the_week, nice_datetime_format

def random_code(length: int, digits: bool = True, letters: bool = True) -> str:
    pool = ''
    if digits:
        pool += string.digits
    if letters:
        pool += string.ascii_uppercase
    if not pool:
        raise ValueError("At least one of 'digits' or 'letters' must be True.")
    return ''.join(random.choices(pool, k=length))

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

pwd_context = CryptContext(["bcrypt"], deprecated="auto")

# Initialize the Argon2 hasher
ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def hash_fast(data: str, salt: str) -> str:
    """
    Use this for fast hashing of tokens, keys, or data integrity.
    Uses keyed BLAKE2b (effectively a fast MAC).
    """
    return hashlib.blake2b(data.encode(), salt=salt.encode()).hexdigest()

def verify(password: str, target: str):
    """
    Takes a password as input and verifies it against the target hash.
    Args:
        password: the password to verify
        target: the hash to verify against

    Returns:
        :bool: True if the password matches the hash, False otherwise
    """
    try:
        result = pwd_context.verify(password, target)
        return result
    except UnknownHashError:
        try:
            return ph.verify(target, password)
        except VerifyMismatchError:
            return False

# Nice datetime helpers
def get_nice_datetime(date_time: datetime, language: str = "en") -> str:
    """
    Returns a nice datetime containing a day of the week and the time.
    Args:
        date_time: the date to get the nice datetime from
        language: the language to use, defaults to 'en'

    Returns:
        str: a nice datetime to read
    """
    day = days_of_the_week[language][date_time.weekday()]
    time_hour = date_time.hour
    time_min = date_time.minute
    moment = "AM"

    match language:
        case "en":
            if time_hour > 12:
                time_hour -= 12
                moment = "PM"
            time = str(time_hour) + ":" + str(time_min) + moment
        case "fr":
            time = str(time_hour) + "h" + str(time_min)
        case _:
            time = str(time_hour) + ":" + str(time_min)

    jinja_template = Environment().from_string(nice_datetime_format[language])
    return jinja_template.render(day=day, time=time)