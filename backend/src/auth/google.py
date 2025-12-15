import requests

from jose import jwt

from backend.config import settings as app_settings
from backend.db.database import get_db
from backend.src.auth.constants import GOOGLE_PUBLIC_KEYS_URL, GOOGLE_TOKEN_ISSUERS
from backend.src.auth.exceptions import GoogleSSOLoginFailedError
from backend.src.auth.schemas import GoogleTokenData
from backend.src.users.utils import get_user_id_from_email


async def verify_google_token(token: str, language: str = "en"):
    """
    Return datas (email, email_verified, sub) of the token if valid and signed by Google.
    :param token: A jwt token.
    :return: GoogleTokenData schema
    """
    # This verification use Google's public keys
    # Note that Google keys regularly rotate, making
    # this function short-term valid only.
    response = requests.get(GOOGLE_PUBLIC_KEYS_URL)
    json_response = response.json()

    try:
        token_header = jwt.get_unverified_header(token)
        token_claims = jwt.get_unverified_claims(token)
    except jwt.JWTError:
        raise GoogleSSOLoginFailedError(language=language)

    kid = token_header["kid"]

    # Find the matching issuer
    iss = next(iss for iss in GOOGLE_TOKEN_ISSUERS if iss == token_claims["iss"]) or None

    # Find the matching key with the right kid
    key = next(k for k in json_response["keys"] if k['kid'] == kid) or None


    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=['RS256'],
            audience=app_settings.google_auth_expo_client_id,
            issuer=iss
        )

        if not payload["email_verified"]:
            raise GoogleSSOLoginFailedError(language=language)

        return GoogleTokenData(**payload)
    except jwt.JWTError:
        raise GoogleSSOLoginFailedError(language=language)

async def google_automatic_password(sub):
    return app_settings.secret_key[:32] + sub

async def get_google_id_from_email(email: str):
    user_id = get_user_id_from_email(email)

    if user_id:
        db = get_db()
        db.cursor.execute("""\
            SELECT * FROM googleids
            WHERE user_id = %s""", (user_id,))
        google_id = db.cursor.fetchone()

        if google_id:
            return google_id
        else:
            return None

    return None

async def get_user_id_from_google_id(google_id: int) -> int | None:
    db = get_db()
    db.cursor.execute("""\
        SELECT user_id
        FROM googleids
        WHERE google_id = %s""", (google_id,))
    user_id = db.cursor.fetchone()

    if not user_id:
        return None

    return int(user_id["user_id"])