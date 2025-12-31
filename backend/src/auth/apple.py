import base64
from datetime import datetime, timedelta, UTC

import requests
from jose import jwt, JWTError

from backend.config import settings as app_settings
from backend.db.database import get_db
from backend.src.auth.constants import APPLE_TOKEN_ISSUER, APPLE_TOKEN_VALIDATION_ENDPOINT, APPLE_PUBLIC_KEYS_URL
from backend.src.auth import exceptions as auth_exceptions
from backend.src.auth.exceptions import AppleSSOLoginFailedError
from backend.src.auth.schemas import AppleIdTokenData, AppleTokenData
from backend.utils import hash_fast


async def create_apple_client_secret(expires_delta: timedelta = timedelta(minutes=app_settings.token_expires_minutes)):
    headers = {
        "alg": "ES256",
        "kid": app_settings.apple_dev_kid
    }
    data = {
        "iss": app_settings.apple_app_iss,
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC) + expires_delta,
        "aud": APPLE_TOKEN_ISSUER,
        "sub": app_settings.apple_dev_sub
    }
    key = base64.b64decode(app_settings.apple_dev_private_key)
    pem_key_content = key.decode('utf-8')

    try:
        encoded_jwt = jwt.encode(claims= data, key= pem_key_content, headers= headers, algorithm= "ES256")
        return encoded_jwt

    except Exception as e:
        print(e)
        # raise JWTError()


async def validate_apple_token(authorization_code: str = None, refresh_token: str = None, language: str = "en") -> AppleTokenData:
    """
    Returns the identity token, an access token, and (optionally) a refresh token if Apple validate an authorization grant code
    or validate an existing refresh token. Required arg is authorization_code OR refresh_token.
    Args:
        authorization_code: (str) when 'Sign in with Apple' successfully, the authorization code given
        refresh_token: (str) The refresh token received from the validation server during an authorization request.
        language: (str) Errors langage translations (defaults to 'en')

    Returns:
        An AppleTokenData schema. example: {
            "access_token": "adg61...67Or9",
            "token_type": "Bearer",
            "expires_in": 3600,
            "refresh_token": "rca7...lABoQ", (only for authorization_code)
            "id_token": "eyJra...96sZg"
        }
    """
    headers = {
        "content-type": "application/x-www-form-urlencoded",
    }
    body = {
        "authorization": {
            "client_id": app_settings.apple_client_id,
            "client_secret": await create_apple_client_secret(
                timedelta(minutes=app_settings.refresh_token_expires_minutes)),
            "code": authorization_code,
            "grant_type": "authorization_code"
        },
        "refresh_token": {
            "client_id": app_settings.apple_client_id,
            "client_secret": await create_apple_client_secret(
                timedelta(minutes=app_settings.refresh_token_expires_minutes)),
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
    }

    if authorization_code:
        response = requests.post(APPLE_TOKEN_VALIDATION_ENDPOINT, headers=headers, data=body["authorization"])

        return AppleTokenData(**response.json())
    if refresh_token:
        response = requests.post(APPLE_TOKEN_VALIDATION_ENDPOINT, headers=headers, data=body["refresh_token"])

        return AppleTokenData(**response.json())

    raise auth_exceptions.AppleSSOLoginFailedError(language= language)


async def verify_apple_id_token(id_token: str, nonce: str, language: str = "en") -> AppleIdTokenData:
    # This verification use Apple's public keys
    response = requests.get(APPLE_PUBLIC_KEYS_URL)
    json_response = response.json()

    try:
        token_header = jwt.get_unverified_header(id_token)
        token_claims = jwt.get_unverified_claims(id_token)
    except jwt.JWTError:
        raise AppleSSOLoginFailedError(language=language)

    kid = token_header["kid"]

    # Find the matching key with the right kid
    key = next(k for k in json_response["keys"] if k['kid'] == kid) or None

    # Check if the nonce is correct
    if not token_claims["nonce"] == hash_fast(nonce, app_settings.apple_dev_nonce_secret):
        raise AppleSSOLoginFailedError(language=language)

    try:
        payload = jwt.decode(
            id_token,
            key,
            algorithms=['ES256'],
            audience=app_settings.apple_client_id,
            issuer=APPLE_TOKEN_ISSUER
        )

        return AppleIdTokenData(**payload)
    except jwt.JWTError:
        raise AppleSSOLoginFailedError(language=language)


async def get_user_id_from_apple_id(apple_id: str) -> int | None:
    db = get_db()
    db.cursor.execute("""\
        SELECT user_id
        FROM appleids
        WHERE apple_id = %s""", (apple_id,))
    user_id = db.cursor.fetchone()

    if not user_id:
        return None

    return int(user_id["user_id"])