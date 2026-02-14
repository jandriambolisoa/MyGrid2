from fastapi import APIRouter, Depends

from backend.constants import QUERY_LIMIT
from backend.db.database import Database, get_db
from backend.oauth2 import get_current_user
from backend.src.users.exceptions import NoUserFoundError
from backend.src.users.schemas import User, UserSelf

router = APIRouter(
    prefix="/users",
    tags= ["users"]
)


@router.get("/search", response_model=list[User])
async def search_users(current_user: UserSelf = Depends(get_current_user), db: Database = Depends(get_db),
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
