import json

import requests
from jinja2 import Environment

from backend.config import settings as app_settings
from backend.db.database import get_db
from backend.exceptions import MicroservicesAreOffException
from backend.oauth2 import create_jwt_token
from backend.src.auth import signals as auth_signals
from backend.src.users import signals as users_signals
from backend.src.auth.texts import mailing_welcome_subject, mailing_welcome_preview, mailing_welcome_body, \
    mailing_welcome_title, mailing_verification_title, mailing_verification_subject, mailing_verification_confirm, \
    mailing_verification_preview, mailing_verification_body
from backend.src.users.exceptions import NoUserFoundError


async def send_welcome_email(user_id: int):
    if app_settings.ms == 0:
        raise MicroservicesAreOffException()

    db = get_db()
    db.cursor.execute("""\
        SELECT username, email, language
        FROM users
        WHERE id = %s""", (user_id,))
    user = db.cursor.fetchone()

    if not user:
        raise NoUserFoundError(language="en")

    preview_text = Environment().from_string(mailing_welcome_preview[user["language"]])
    title_text = Environment().from_string(mailing_welcome_title[user["language"]])

    datas = {
        "receiver": user["email"],
        "subject": mailing_welcome_subject[user["language"]],
        "fields": {
            "PREVIEW_TEXT": preview_text.render(USERNAME = user["username"]),
            "IMAGE_URL": "https://assets.zyrosite.com/k1JwmslwXt9ap0c7/image001_cropped-0yQk2HgfVSB60du7.jpg",
            "BODY": mailing_welcome_body[user["language"]],
            "TITLE": title_text.render(USERNAME = user["username"])
        }
    }
    print("# INFO: Sending welcome email")
    try:
        requests.post(f"{app_settings.ms_mailings_url}/sending/simple", data=json.dumps(datas))
    except requests.exceptions.ConnectionError as err:
        print("# ERROR: %s"%err)

async def send_verification_email(user_id: int):
    if app_settings.ms == 0:
        raise MicroservicesAreOffException()

    db = get_db()
    db.cursor.execute("""\
        SELECT *
        FROM users
        WHERE id = %s""", (user_id,))
    user = db.cursor.fetchone()

    token_datas = {
        "user_id": user["id"],
        "username": user["username"],
        "language": user["language"]
    }
    token = await create_jwt_token(token_datas)

    if not user:
        raise NoUserFoundError(language="en")

    title_text = Environment().from_string(mailing_verification_title[user["language"]])

    datas = {
        "receiver": user["email"],
        "subject": mailing_verification_subject[user["language"]],
        "fields": {
            "CONFIRM_TEXT": mailing_verification_confirm[user["language"]],
            "PREVIEW_TEXT": mailing_verification_preview[user["language"]],
            "BODY": mailing_verification_body[user["language"]],
            "IMAGE_URL": "https://assets.zyrosite.com/k1JwmslwXt9ap0c7/image002-bei8YY9PHwG3h1T8.png",
            "TITLE": title_text.render(USERNAME = user["username"]),
            "CONFIRM_URL": f"{app_settings.confirmed_email_url}?token={token}"
        }
    }
    print("# INFO: Sending welcome email")
    try:
        requests.post(f"{app_settings.ms_mailings_url}/sending/confirm", data=json.dumps(datas))
    except requests.exceptions.ConnectionError as err:
        print("# ERROR: %s" % err)


def init_listener():
    auth_signals.validate_mail.connect(send_welcome_email)
    users_signals.created.connect(send_verification_email)