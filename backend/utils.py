import string
import random
import hashlib
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from passlib.context import CryptContext
from passlib.exc import UnknownHashError


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
