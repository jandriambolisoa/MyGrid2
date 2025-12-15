import string
import random

from passlib.context import CryptContext
from passlib.hash import sha256_crypt

def random_code(length: int, digits: bool = True, letters: bool = True) -> str:
    pool = ''
    if digits:
        pool += string.digits
    if letters:
        pool += string.ascii_uppercase
    if not pool:
        raise ValueError("At least one of 'digits' or 'letters' must be True.")
    return ''.join(random.choices(pool, k=length))

pwd_context = CryptContext(["bcrypt"], deprecated="auto")

def hash(input: str):
    return pwd_context.hash(input)

def nonce_hash(input: str, salt: str):
    return sha256_crypt.using(salt=salt).hash(input)

def verify(input: str, target: str):
    return pwd_context.verify(input, target)
