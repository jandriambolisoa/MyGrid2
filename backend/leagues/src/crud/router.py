from fastapi import APIRouter, Depends

from backend.constants import QUERY_LIMIT
from backend.db.database import get_db, Database
from backend.leagues.schemas import League

router = APIRouter(
    prefix="/crud",
    tags= ["CRUD"]
)


@router.get("/", response_model=list[League])
async def search_leagues(db: Database = Depends(get_db),
                 q: str = "",
                 limit: int = QUERY_LIMIT,
                 page: int = 0):
    search = "%" + q + "%"
    offset = limit * page

    db.cursor.execute("""
        SELECT *
        FROM users
        WHERE username LIKE %s
        AND id NOT IN (
            SELECT DISTINCT ON (bannedhistory.user_id) bannedhistory.user_id AS id
            FROM bannedhistory
            WHERE bannedhistory.banned = true            
            ORDER BY bannedhistory.user_id, bannedhistory.created DESC
            )
        EXCEPT
        SELECT *
        FROM users
        WHERE id = %s
        ORDER BY username ASC
        LIMIT %s OFFSET %s""", (search, current_user.id, limit, offset))
    results = db.cursor.fetchall()

    if not results:
        raise NoUserFoundError(current_user.language)

    # TODO : Implement full profile

    return results

