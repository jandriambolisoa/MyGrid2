from emoji import is_emoji
from fastapi import Depends, APIRouter
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy import ForeignKey
from starlette import status

from backend.db.database import Database, get_db
from backend.oauth2 import get_current_user
from backend.src.events.dependencies import valid_session_id, is_session_over
from backend.src.predictions.dependencies import is_user_has_prono
from backend.src.predictions.exceptions import NoPredictionError, PredictionNotAvailableError
from backend.src.reactions.exceptions import ReactionIsNotAnEmojiError
from backend.src.reactions.schemas import PostReaction
from backend.src.reactions import signals as reactions_signals
from backend.src.users.dependencies import valid_user_id, get_current_user_language
from backend.src.users.schemas import UserSelf

router = APIRouter(
    prefix="/events/sessions/predictions/reaction",
    tags= ["reaction"]
)

@router.post("/{session_id}", status_code=status.HTTP_200_OK)
async def add_user_session_reaction(reaction: PostReaction, session_id: int = Depends(valid_session_id), user_id: int = Depends(valid_user_id), language: str = Depends(get_current_user_language), db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not user_id:
        user_id = current_user.id

    if not await is_user_has_prono(user_id, session_id):
        raise NoPredictionError(language= language)

    if not await is_session_over(session_id):
        raise PredictionNotAvailableError(language= language)

    if not is_emoji(reaction.reaction):
        raise ReactionIsNotAnEmojiError(reaction.reaction, language= language)

    try:
        db.cursor.execute("""\
            INSERT INTO sessionsreactions (user_id, session_id, by, reaction)
            VALUES (%s, %s, %s, %s)""", (user_id, session_id, current_user.id, reaction.reaction))
        db.conn.commit()
    except UniqueViolation:
        db.conn.rollback()
        db.cursor.execute("""\
            UPDATE sessionsreactions
            SET reaction = %s
            WHERE user_id = %s AND session_id = %s AND by = %s""", (reaction.reaction, user_id, session_id, current_user.id))
        db.conn.commit()

    if user_id != current_user.id:
        await reactions_signals.user_reacted.send(user_id=user_id, session_id=session_id, emoji=reaction.reaction)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_session_reaction(session_id: int = Depends(valid_session_id), user_id: int = Depends(valid_user_id), language: str = Depends(get_current_user_language), db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not user_id:
        user_id = current_user.id

    db.cursor.execute("""\
        DELETE FROM sessionsreactions
        WHERE user_id = %s AND session_id = %s AND by = %s""", (user_id, session_id, current_user.id))
    db.conn.commit()