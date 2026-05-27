from fastapi.params import Depends

from backend.db.database import get_db
from backend.src.users.dependencies import valid_user_id
from backend.utils import random_code


async def create_unique_invite_code():
    """
    Create and return a unique invite code
    :return: str
    """
    db = get_db()
    db.cursor.execute("""
        SELECT code FROM leaguesinvites""")
    all_invite_codes = db.cursor.fetchall()
    all_invite_codes = [index["code"] for index in all_invite_codes]

    new_invite_code = random_code(9)
    while new_invite_code in all_invite_codes:
        new_invite_code = random_code(9)

    return new_invite_code

async def get_users_leagues_count(user_id: int) -> int:
    db = get_db()
    db.cursor.execute("""\
        SELECT COUNT(*) AS nb
        FROM leaguesusers 
        WHERE user_id = %s
        AND organizer = true""", (user_id,))
    result = db.cursor.fetchone()

    if not result:
        return 0

    return result["nb"]