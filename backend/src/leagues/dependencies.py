from fastapi import Depends

from backend.db.database import get_db
from backend.oauth2 import get_current_user
from backend.src.leagues.exceptions import LeagueDoesNotExistsError
from backend.src.users.schemas import UserSelf


async def valid_league_id(league_id: int, language: str = "en") -> int:
    db = get_db()
    db.cursor.execute("""
        SELECT id FROM leagues
        WHERE id = %s""", (league_id,))
    league = db.cursor.fetchone()
    if not league:
        raise LeagueDoesNotExistsError(language=language, league_id=league_id)

    return league_id

async def owned_league_id(league_id: int = Depends(valid_league_id), current_user: UserSelf = Depends(get_current_user), language: str = "en") -> int:
    db = get_db()
    db.cursor.execute("""
        SELECT league_id FROM leaguesusers
        WHERE user_id = %s
        AND league_id = %s
        AND organizer = true""", (current_user.id, league_id,))
    league = db.cursor.fetchone()
    if not league:
        raise LeagueNotOwnedError(language=language, league_id=league_id)

    return league_id