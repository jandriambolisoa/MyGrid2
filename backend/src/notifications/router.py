from typing import Union

from fastapi import APIRouter, Depends, status

from backend.db.database import Database, get_db
from backend.exceptions import ForbiddenAccessException
from backend.oauth2 import get_current_user
from backend.src.notifications.dependencies import valid_push_token
from backend.src.notifications.schemas import PushNotification, PushToken
from backend.src.users.dependencies import get_current_user_language
from backend.src.users.privileges import is_user_moderator_or_admin
from backend.src.users.schemas import UserSelf
from backend.src.predictions.schemas import PredictionSession, PredictionScoreSession

router = APIRouter(
    prefix="/notifications",
    tags= ["notifications"]
)

#
# CRUD operations
#

@router.post("/push", status_code=status.HTTP_200_OK)
async def register_push_token_notification(to_register: PushToken, language: str = Depends(get_current_user_language), db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    token = await valid_push_token(to_register.token, language)

    # Delete old push token
    db.cursor.execute("""\
        DELETE FROM pushtokens
        WHERE user_id = %s""", (current_user.id,))
    db.conn.commit()

    db.cursor.execute("""\
        INSERT INTO pushtokens (user_id, token)
        VALUES (%s, %s)""",(current_user.id, token))
    db.conn.commit()