from typing import List

from backend.db.database import get_db
from backend.src.manager.constants import MAX_POOL_SIZE
from backend.src.notifications.exceptions import NotAValidPushTokenError
from backend.src.notifications.schemas import PushToken, UserEmail


async def valid_push_token(token: str, language: str = "en") -> str:
    if token.startswith("ExponentPushToken["):
        return token

    raise NotAValidPushTokenError(language)


async def get_all_push_tokens(limit: int = MAX_POOL_SIZE) -> List[PushToken]:
    db = get_db()
    db.cursor.execute("""\
        SELECT pushtokens.token, 
        users.language
        FROM pushtokens
        LEFT JOIN users ON pushtokens.user_id = users.id
        LIMIT %s""", (limit,))
    tokens = db.cursor.fetchall()

    return [PushToken(**token) for token in tokens]

async def get_all_verified_emails(limit: int = MAX_POOL_SIZE) -> List[UserEmail]:
    db = get_db()
    db.cursor.execute("""\
        SELECT username, email, language
        FROM users
        WHERE verified = true
        LIMIT %s""", (limit,))
    emails = db.cursor.fetchall()

    return [UserEmail(**email) for email in emails]