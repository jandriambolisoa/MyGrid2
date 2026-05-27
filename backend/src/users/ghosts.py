from datetime import datetime, UTC

from backend.db.database import get_db
from backend.obligations import create_obligation, Obligation


async def ghost_user_validator(user_id: int, language: str = "en"):
    db = get_db()

    db.cursor.execute("SELECT exp FROM ghostusers WHERE user_id = %s", (user_id,))
    exp = db.cursor.fetchone()[0]

    exp_datetime = datetime.fromisoformat(exp)
    if datetime.now(UTC) > exp_datetime:
        await create_obligation(code="convertuser", user_id=user_id, language= language)

        raise Obligation("convertuser", language=language)