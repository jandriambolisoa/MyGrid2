import requests

from backend.constants import MAIL_VERIFICATION, MAIL_WELCOME
from backend.src.auth import signals as auth_signals
from backend.src.users.schemas import UserSelf
from backend.src.users import signals as users_signals
from backend.config import settings as app_settings
from backend.oauth2 import create_jwt_token

async def send_verification_email(user: UserSelf):
    token_datas = {
        "username": user.username,
        "email": user.email,
        "language": user.language
    }
    token = await create_jwt_token(token_datas)

    fields = {
        "username": user.username,
        "token": token
    }
    response = requests.post(
        f"{app_settings.ms_mailings_url}/sending/{MAIL_VERIFICATION}",
        params=fields,
        language=user.language
    )

    if response.status_code != 200:
        #TODO: logging system
        raise RuntimeError(f"Mail verification failed with status code {response.status_code}")

users_signals.created.connect(send_verification_email)

async def send_welcome_email(user: UserSelf):
    fields = {
        "username": user.username
    }
    response = requests.post(
        f"{app_settings.ms_mailings_url}/sending/{MAIL_WELCOME}",
        params=fields,
        language=user.language
    )

    if response.status_code != 200:
        #TODO: logging system
        raise RuntimeError(f"Mail verification failed with status code {response.status_code}")

auth_signals.validate_mail.connect(send_welcome_email)