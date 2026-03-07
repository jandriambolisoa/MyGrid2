import asyncio
import json
from typing import Union

import requests
from requests import HTTPError, ConnectionError
from exponent_server_sdk import PushClient, PushMessage, PushServerError, DeviceNotRegisteredError, PushTicketError
from fastapi import APIRouter, Depends, status

from backend.db.database import Database, get_db
from backend.exceptions import ForbiddenAccessException, MicroservicesAreOffException
from backend.oauth2 import get_current_user
from backend.config import settings as app_settings
from backend.src.manager.constants import MAX_POOL_SIZE, MAX_PUSH_NOTIFICATIONS_ATTEMPTS, \
    PUSH_NOTIFICATION_BACKOFF_BASE, PUSH_NOTIFICATION_BACKOFF_CAP
from backend.src.notifications.dependencies import get_all_push_tokens, get_all_verified_emails
from backend.src.notifications.schemas import PushNotification, SimpleEmail
from backend.src.users.dependencies import get_current_user_language
from backend.src.users.exceptions import NoUserFoundError
from backend.src.users.privileges import is_user_moderator_or_admin
from backend.src.users.schemas import UserSelf
from backend.src.predictions.schemas import PredictionSession, PredictionScoreSession
from backend.utils import exponential_backoff

router = APIRouter(
    prefix="/manager",
    tags= ["manager"]
)

#
# CRUD operations
#

@router.post("/notification/push/send", status_code=status.HTTP_200_OK)
async def send_global_push_notification(to_send: PushNotification, language: str = Depends(get_current_user_language), db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language= language)

    tokens = await get_all_push_tokens(MAX_POOL_SIZE)

    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {app_settings.expo_access_token}",
            "accept": "application/json",
            "accept-encoding": "gzip, deflate",
            "content-type": "application/json",
        }
    )

    print("# PUSH NOTIFICATIONS: start")
    print(f"#\t{to_send.title['en']}")
    print(f"#\t{to_send.body['en']}")

    for token in tokens:
        # Limit the number of attempt in an exponential backoff
        # For each attempt, send a request and make sure it's sent
        # to expo API. Retry if an internet error occured.
        attempt = 0
        while attempt < MAX_PUSH_NOTIFICATIONS_ATTEMPTS:
            attempt += 1
            try:
                # Try to send Push notification
                response = PushClient(session=session).publish(
                    PushMessage(
                        to=token.token,
                        title=to_send.title.get(token.language, to_send.title["en"]),
                        body=to_send.body.get(token.language, to_send.body["en"])
                    )
                )

                # Verify response quality
                response.validate_response()
                break

            except PushServerError as error:
                # Encountered some likely formatting/validation error.
                break

            except (ConnectionError, HTTPError) as error:
                # Encountered some Connection or HTTP error
                await asyncio.sleep(await exponential_backoff(attempt, PUSH_NOTIFICATION_BACKOFF_CAP, PUSH_NOTIFICATION_BACKOFF_BASE))  # Retry

            except (DeviceNotRegisteredError, ValueError):
                # Delete the push token from our database
                db.cursor.execute("""
                    DELETE FROM pushtokens
                    WHERE token = %s
                    """, (token.token,))
                db.conn.commit()
                break

            except PushTicketError as error:
                # Encountered some other per-notification error.
                print(f"Error report:\n{token.token}\nAttempt: {attempt}\n{error.push_response._asdict()}")
                await asyncio.sleep(await exponential_backoff(attempt, PUSH_NOTIFICATION_BACKOFF_CAP, PUSH_NOTIFICATION_BACKOFF_BASE)) # Retry

        print("# PUSH NOTIFICATIONS: end")


@router.post("/notification/mail/simple/send", status_code=status.HTTP_200_OK)
async def send_global_simple_email(to_send: SimpleEmail, current_user: UserSelf = Depends(get_current_user)):
    if not is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language= "en")

    if app_settings.ms == 0:
        raise MicroservicesAreOffException()

    emails = await get_all_verified_emails(MAX_POOL_SIZE)

    if not emails:
        raise NoUserFoundError(language="en")

    for email in emails:
        datas = {
            "receiver": email.email,
            "subject": to_send.subject.get(email.language, to_send.subject["en"]),
            "fields": {
                "PREVIEW_TEXT": to_send.preview.get(email.language, to_send.preview["en"]),
                "IMAGE_URL": to_send.image_url,
                "BODY": to_send.body.get(email.language, to_send.body["en"]),
                "TITLE": to_send.title.get(email.language, to_send.title["en"])
            }
        }
        try:
            requests.post(f"{app_settings.ms_mailings_url}/sending/simple", data=json.dumps(datas))
        except requests.exceptions.ConnectionError:
            pass