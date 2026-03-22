from typing import List

from backend.db.database import get_db
from backend.src.reactions.schemas import UserReaction
from backend.src.users.dependencies import get_user_from_id
from backend.src.users.schemas import User

async def is_user_reacted_to_prediction(current_user_id: int, session_id: int, prediction_user_id: int) -> bool:
    db = get_db()
    db.cursor.execute("""\
        SELECT * FROM sessionsreactions
        WHERE session_id = %s AND user_id = %s AND by = %s""",(session_id, prediction_user_id, current_user_id))
    reaction = db.cursor.fetchone()

    if not reaction:
        return False

    return True

async def get_user_prediction_reactions(user_id: int, session_id: int) -> List[UserReaction] | None:
    db = get_db()
    db.cursor.execute("""\
        SELECT sessionsreactions.reaction,
        users.id AS user_id,
        users.username AS user_username,
        users.created AS user_created,
        users.image AS user_image
        FROM sessionsreactions
        LEFT JOIN users ON sessionsreactions.by = users.id
        WHERE sessionsreactions.session_id = %s AND sessionsreactions.user_id = %s
        ORDER BY sessionsreactions.created DESC""",(session_id, user_id))
    reactions = db.cursor.fetchall()

    if not reactions:
        return None

    return [
        UserReaction(
            user=User(**{key.removeprefix("user_"): reaction[key] for key in reaction.keys() if key.startswith("user_")}),
            reaction=reaction["reaction"])
        for reaction in reactions
    ]