from fastapi import APIRouter, Depends
from psycopg.errors import UniqueViolation
from starlette import status

from backend.constants import QUERY_LIMIT
from backend.db.database import get_db, Database
from backend.oauth2 import get_current_user
from backend.src.leagues.constants import MAX_LEAGUE_CREATION
from backend.src.leagues.schemas import League, LeagueCreate, LeagueUpdate
from backend.src.leagues.dependencies import valid_league_id, owned_league_id
from backend.src.leagues.exceptions import NoLeagueFoundError, MaxLeagueCreationError, LeagueAlreadyExistsError
from backend.src.leagues.syntax import valid_league_name
from backend.src.leagues.utils import get_users_leagues_count
from backend.src.leagues import signals as leagues_signals
from backend.src.users.dependencies import get_current_user_language
from backend.src.users.schemas import UserSelf


router = APIRouter(
    prefix="/leagues",
    tags= ["leagues"]
)

@router.post("", response_model=League, status_code=status.HTTP_201_CREATED)
async def create_league(
        to_create: LeagueCreate,
        language: str = Depends(get_current_user_language),
        db: Database = Depends(get_db),
        current_user: UserSelf = Depends(get_current_user)):
    # Verify user's league creation count
    # TODO check user privilege if he's trying to create multiple leagues
    if await get_users_leagues_count(current_user.id) >= MAX_LEAGUE_CREATION:
        raise MaxLeagueCreationError(language)

    league_name = await valid_league_name(to_create.name)

    try:
        db.cursor.execute("""\
            INSERT INTO leagues (name, description, colors, private)
            VALUES (%s, %s, %s, %s)
            RETURNING *""", (league_name, to_create.description, to_create.colors, to_create.private))
        created = db.cursor.fetchone()

        db.conn.commit()
    except UniqueViolation:
        db.conn.rollback()
        raise LeagueAlreadyExistsError(language=language)

    await leagues_signals.create_league.send(created, user=current_user)
    return created


@router.get("", response_model=list[League])
async def search_leagues(db: Database = Depends(get_db),
                 q: str = "",
                 language: str = "en",
                 limit: int = QUERY_LIMIT,
                 page: int = 0):
    search = "%" + q + "%"
    offset = limit * page

    db.cursor.execute("""
        SELECT *
        FROM leagues
        WHERE name LIKE %s
        ORDER BY name ASC
        LIMIT %s OFFSET %s""", (search, limit, offset))
    results = db.cursor.fetchall()

    if not results:
        raise NoLeagueFoundError(language)

    return results

@router.get("/{league_id}", response_model=League)
async def get_league(
        league_id: int = Depends(valid_league_id),
        db: Database = Depends(get_db),
        q: str = "",
        language: str = "en"):

    db.cursor.execute("""
        SELECT *
        FROM leagues
        WHERE id = %s
        """, (league_id,))
    league = db.cursor.fetchone()

    if not league:
        raise NoLeagueFoundError(language)

    return league

@router.put("/{league_id}", response_model=League)
async def update_league(
        update_data: LeagueUpdate,
        league_id: int = Depends(owned_league_id),
        language: str = Depends(get_current_user_language),
        db: Database = Depends(get_db),
        current_user: UserSelf = Depends(get_current_user)):
    db.cursor.execute("SELECT * FROM leagues WHERE id = %s", (league_id,))
    existing = db.cursor.fetchone()

    new_name = update_data.name if update_data.name is not None else existing["name"]
    new_description = update_data.description if update_data.description is not None else existing["description"]
    new_colors = update_data.colors if update_data.colors is not None else existing["colors"]
    new_private = update_data.private if update_data.private is not None else existing["private"]

    if new_name != existing["name"]:
        new_name = await valid_league_name(new_name)

    try:
        db.cursor.execute("""
            UPDATE leagues
            SET name = %s, description = %s, colors = %s, private = %s
            WHERE id = %s
            RETURNING *
        """, (new_name, new_description, new_colors, new_private, league_id))
        updated = db.cursor.fetchone()
        db.conn.commit()
    except UniqueViolation:
        db.conn.rollback()
        raise LeagueAlreadyExistsError(language=language)

    await leagues_signals.update_league.send(updated, user=current_user)
    return updated

@router.delete("/{league_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_league(
        league_id: int = Depends(owned_league_id),
        db: Database = Depends(get_db),
        current_user: UserSelf = Depends(get_current_user)):
    db.cursor.execute("DELETE FROM leagues WHERE id = %s RETURNING *", (league_id,))
    deleted = db.cursor.fetchone()
    db.conn.commit()

    await leagues_signals.delete_league.send(deleted, user=current_user)