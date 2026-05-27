import string

from backend.db.database import get_db
from backend.src.leagues.constants import LEAGUE_NAME_MAX_LENGTH
from backend.src.leagues.exceptions import NotAValidLeagueNameLengthError, NotAValidLeagueNameCharactersError, \
    NotAvailableLeagueNameError


async def valid_league_name(league_name: str, language: str = "en") -> str:
    if len(league_name) > LEAGUE_NAME_MAX_LENGTH:
        raise NotAValidLeagueNameLengthError(language=language)

    authorized_characters = [*string.ascii_lowercase, *string.ascii_uppercase, *string.digits, "_", "-", " "]

    for character in league_name:
        if not character in authorized_characters:
            raise NotAValidLeagueNameCharactersError(language=language)

    db = get_db()

    db.cursor.execute("""
        SELECT bannedusernames.username
        FROM bannedusernames
        WHERE bannedusernames.username = %s
        UNION
        SELECT leagues.name
        FROM leagues
        WHERE leagues.name = %s""", (league_name, league_name))
    is_unavailable = db.cursor.fetchone()

    if is_unavailable:
        raise NotAvailableLeagueNameError(language=language)

    return league_name
