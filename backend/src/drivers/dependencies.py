from backend.db.database import get_db
from backend.src.drivers.constants import CODENAME_LENGTH
from backend.src.drivers.exceptions import NotAValidCodenameLengthError, NotAValidColorError, DriverNotFoundError, \
    DriverDoesNotExistsError


async def valid_codename(codename: str, language: str = "en") -> str:
    if codename != CODENAME_LENGTH:
        raise NotAValidCodenameLengthError(language=language)

    return codename

async def valid_color(color: str, language: str = "en") -> str:
    """
    Verify if the color is a hexadecimal color.
    :param color: The hexadecimal color value.
    :param language: The language of the user.
    :return: The hexadecimal color value.
    """
    color = color.upper()
    color = color.lstrip("#")

    if len(color) != 6:
        raise NotAValidColorError(language=language)

    return f"#{color}"

async def valid_driver_id(driver_id: int, language: str = "en") -> int:
    db = get_db()
    db.cursor.execute("""
        SELECT id FROM drivers
        WHERE id = %s""", (driver_id,))
    driver = db.cursor.fetchone()
    if not driver:
        raise DriverDoesNotExistsError(language=language, driver_id=driver_id)

    return driver_id

async def valid_team_id(team_id: int, language: str = "en") -> int:
    db = get_db()
    db.cursor.execute("""
        SELECT id FROM teams
        WHERE id = %s""", (team_id,))
    team = db.cursor.fetchone()
    if not team:
        raise TeamDoesNotExistsError(language=language, team_id=team_id)

    return team_id