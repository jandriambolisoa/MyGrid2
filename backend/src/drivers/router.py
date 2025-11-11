from fastapi import APIRouter, status, Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from backend.db.database import get_db, Database
from backend.exceptions import ForbiddenAccessException
from backend.oauth2 import get_current_user
from backend import exceptions as app_exceptions
from backend.constants import QUERY_LIMIT
from backend.src.drivers.exceptions import DriverNotFoundError, TeamNotFoundError, DriverAlreadyExistsError, \
    TeamAlreadyExistsError
from backend.src.users.privileges import is_user_moderator_or_admin
from backend.src.drivers.dependencies import valid_codename, valid_color
from backend.src.drivers.schemas import (
    Team, Driver, DriversTeams, DriverCreate, TeamCreate, TeamsDrivers, DriverUpdate, TeamUpdate
)
from backend.src.drivers import signals as drivers_signals
from backend.src.users.schemas import UserSelf

router = APIRouter(
    prefix="/drivers",
    tags= ["drivers"]
)

#
# CRUD operations
#

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Driver)
async def create_driver(driver: DriverCreate, language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    await valid_codename(driver.codename, language=language)

    try:
        db.cursor.execute("""
            INSERT INTO drivers (firstname, lastname, codename)
            VALUES (%s, %s, %s)
            RETURNING *
        """, (driver.firstname.title(), driver.lastname.upper(), driver.codename.upper()))
        created_driver = db.cursor.fetchone()

        db.conn.commit()
    except UniqueViolation:
        raise DriverAlreadyExistsError(language=language)

    await drivers_signals.create_driver.send(driver)
    return created_driver


@router.post("/teams", status_code=status.HTTP_201_CREATED, response_model=Team)
async def create_team(team: TeamCreate, language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    await valid_color(team.color, language=language)

    try:
        db.cursor.execute("""
            INSERT INTO teams (name, color)
            VALUES (%s, %s)
            RETURNING *
        """, (team.name.title(), team.color))
        created_team = db.cursor.fetchone()

        db.conn.commit()
    except UniqueViolation:
        raise TeamAlreadyExistsError(language=language)

    await drivers_signals.create_team.send(team)
    return created_team


@router.get("/search", response_model=list[DriversTeams])
async def search_driver(db:Database = Depends(get_db),
        language: str = "en",
        q: str = "",
        limit: int = QUERY_LIMIT,
        page: int = 0):

    search = "%" + q + "%"
    offset = limit * page

    db.cursor.execute("""\
        SELECT sessionsregistrations.driver_id AS driver_id,
        drivers.firstname AS driver_firstname,
        drivers.lastname AS driver_lastname,
        drivers.codename AS driver_codename,
        teams.id AS team_id,
        teams.color AS team_color,
        teams.name AS team_name FROM sessionsregistrations
        LEFT JOIN drivers ON drivers.id = sessionsregistrations.driver_id
        LEFT JOIN teams ON teams.id = sessionsregistrations.team_id
        WHERE LOWER(drivers.firstname||' '||drivers.lastname||' '||drivers.codename)
        LIKE LOWER(%s)
        GROUP BY sessionsregistrations.driver_id, drivers.firstname, drivers.lastname, drivers.codename, teams.id, teams.name, teams.color
        LIMIT %s OFFSET %s;""", (search, limit, offset))
    results = db.cursor.fetchall()

    if not results:
        raise DriverNotFoundError(language=language)

    # Convert result into DriversTeams schemas
    search_results = dict()
    for result in results:
        driver = {key.removeprefix("driver_"): result[key] for key in result.keys() if key.startswith("driver_")}
        team = {key.removeprefix("team_"): result[key] for key in result.keys() if key.startswith("team_")}

        if driver["id"] not in search_results.keys():
            search_results[result["driver_id"]] = {**driver, "teams": [team]}
        else:
            search_results[driver["id"]]["teams"].append(team)

    return list(search_results.values())


@router.get("/teams/search", response_model=list[TeamsDrivers])
async def search_team(db:Database = Depends(get_db),
        language: str = "en",
        q: str = "",
        limit: int = QUERY_LIMIT,
        page: int = 0):

    search = "%" + q + "%"
    offset = limit * page

    db.cursor.execute("""\
        SELECT sessionsregistrations.driver_id AS driver_id,
        drivers.firstname AS driver_firstname,
        drivers.lastname AS driver_lastname,
        drivers.codename AS driver_codename,
        teams.id AS team_id,
        teams.color AS team_color,
        teams.name AS team_name FROM sessionsregistrations
        LEFT JOIN drivers ON drivers.id = sessionsregistrations.driver_id
        LEFT JOIN teams ON teams.id = sessionsregistrations.team_id
        WHERE LOWER(teams.name)
        LIKE LOWER(%s)
        GROUP BY sessionsregistrations.driver_id, drivers.firstname, drivers.lastname, drivers.codename, teams.id, teams.name, teams.color
        LIMIT %s OFFSET %s;""", (search, limit, offset))
    results = db.cursor.fetchall()

    if not results:
        raise TeamNotFoundError(language=language)

    # Convert result into DriversTeams schemas
    search_results = dict()
    for result in results:
        driver = {key.removeprefix("driver_"): result[key] for key in result.keys() if key.startswith("driver_")}
        team = {key.removeprefix("team_"): result[key] for key in result.keys() if key.startswith("team_")}

        if team["id"] not in search_results.keys():
            search_results[result["team_id"]] = {**team, "drivers": [driver]}
        else:
            search_results[team["id"]]["drivers"].append(driver)

    return list(search_results.values())

@router.put("/{id}", response_model=Driver)
async def update_driver(id: int, datas: DriverUpdate, language: str = "en", db:Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    # Get orig driver
    db.cursor.execute("""\
        SELECT * FROM drivers
        WHERE id = %s""", (id,))
    orig = db.cursor.fetchone()

    if not orig:
        raise DriverNotFoundError(language=language)

    # Get default values
    if not datas.firstname:
        datas.firstname = orig["firstname"]
    if not datas.lastname:
        datas.lastname = orig["lastname"]
    if not datas.codename:
        datas.codename = orig["codename"]

    try:
        db.cursor.execute("""\
            UPDATE drivers
            SET firstname = %s, lastname = %s, codename = %s
            WHERE id = %s
            RETURNING *
            """, (datas.firstname, datas.lastname, datas.codename, id))
        updated = db.cursor.fetchone()
        db.conn.commit()

    except UniqueViolation:
        db.conn.rollback()
        raise DriverAlreadyExistsError(language=language)

    return updated


@router.put("/teams/{id}", response_model=Team)
async def update_team(id: int, datas: TeamUpdate, language: str = "en", db:Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    # Get orig team
    db.cursor.execute("""\
        SELECT * FROM teams
        WHERE id = %s""", (id,))
    orig = db.cursor.fetchone()

    if not orig:
        raise TeamNotFoundError(language=language)

    # Get default values
    if not datas.name:
        datas.name = orig["name"]
    if not datas.color:
        datas.color = orig["color"]

    try:
        db.cursor.execute("""\
            UPDATE teams
            SET name = %s, color = %s
            WHERE id = %s
            RETURNING *
            """, (datas.name, await valid_color(datas.color, language=language), id))
        updated = db.cursor.fetchone()
        db.conn.commit()

    except UniqueViolation:
        db.conn.rollback()
        raise TeamAlreadyExistsError(language=language)

    return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_driver(id: int, language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    db.cursor.execute("""
        DELETE FROM drivers
        WHERE id = %s
        RETURNING *""", (id,))
    to_delete = db.cursor.fetchone()

    if not to_delete:
        raise DriverNotFoundError(language=language)

    db.conn.commit()
    drivers_signals.delete_driver.send(driver=to_delete)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/teams/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(id: int, language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise ForbiddenAccessException(language=language)

    db.cursor.execute("""
        DELETE FROM teams
        WHERE id = %s
        RETURNING *""", (id,))
    to_delete = db.cursor.fetchone()

    if not to_delete:
        raise TeamNotFoundError(language=language)

    db.conn.commit()
    await drivers_signals.delete_team.send(team=to_delete)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

