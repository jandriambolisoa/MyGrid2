from backend.db.database import get_db
from backend.src.drivers.constants import CODENAME_LENGTH
from backend.src.drivers.exceptions import NotAValidCodenameLengthError, NotAValidColorError, DriverNotFoundError, \
    DriverDoesNotExistsError, TeamDoesNotExistsError
from backend.src.drivers.schemas import Driver, Team
from backend.src.registrations.schemas import RegistrationDriver


async def valid_codename(codename: str, language: str = "en") -> str:
    if len(codename) != CODENAME_LENGTH:
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


async def get_driver_registration_from_codename(session_id: int, codename: str) -> RegistrationDriver | None:
    db = get_db()
    db.cursor.execute("""
        SELECT drivers.id AS driver_id,
        drivers.firstname AS driver_firstname,
        drivers.lastname AS driver_lastname,
        drivers.codename AS driver_codename,
        teams.id AS team_id,
        teams.name AS team_name,
        teams.color AS team_color,
        sessionsregistrations.prediction AS prediction
        FROM sessionsregistrations
        LEFT JOIN drivers ON drivers.id = sessionsregistrations.driver_id
        LEFT JOIN teams ON teams.id = sessionsregistrations.team_id
        WHERE sessionsregistrations.session_id = %s AND drivers.codename = %s""", (session_id, codename))
    result = db.cursor.fetchone()

    if result:
        driver = {k.removeprefix("driver_"): v for k, v in result if k.startswith("driver_")}
        team = {k.removeprefix("team_"): v for k, v in result if k.startswith("team_")}
        return RegistrationDriver(
            driver_id=driver["driver_id"],
            team_id=team["team_id"],
            driver= Driver(**driver),
            team= Team(**team),
            prediction= result["prediction"]
        )
    else:
        return None