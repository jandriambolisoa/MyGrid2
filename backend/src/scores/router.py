from fastapi import APIRouter, Depends, status
from psycopg.errors import UniqueViolation, ForeignKeyViolation

from backend.db.database import Database, get_db
from backend import exceptions as app_exceptions
from backend.oauth2 import get_current_user
from backend.src.events.dependencies import valid_session_id, valid_championship_id
from backend.src.results.exceptions import NoResultsFoundError, InvalidSessionResultsAttemptError
from backend.src.results.schemas import ResultSession, ResultPost
from backend.src.scores.core import score_parameters_of_a_championship
from backend.src.scores.exceptions import NoParametersFoundError
from backend.src.scores.schemas import ScoresParameters
from backend.src.users.privileges import is_user_moderator_or_admin
from backend.src.users.schemas import UserSelf
from backend.src.results import signals as results_signals

router = APIRouter(
    prefix="/scores",
    tags= ["scores"]
)

#
# CRUD operations
#

@router.get("/parameters/{championship_id}", response_model=ScoresParameters)
async def get_score_parameters_of_a_championship(championship_id: int = Depends(valid_championship_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    return await score_parameters_of_a_championship(championship_id, db, language)


@router.post("/parameters/{championship_id}", status_code=status.HTTP_201_CREATED)
async def override_score_parameters_of_a_championship(parameters: ScoresParameters, championship_id: int = Depends(valid_championship_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if not await is_user_moderator_or_admin(current_user.id):
        raise app_exceptions.ForbiddenAccessException(language=language)

    # Remove old session results
    db.cursor.execute("""
        DELETE
        FROM scoresparameters
        WHERE championship_id = %s""", (championship_id,))
    db.conn.commit()

    for parameter in list(vars(parameters).keys()):
        points_list = getattr(parameters, parameter)
        points_list.sort(reverse=True)

        db.cursor.execute("""
            INSERT INTO scoresparameters (championship_id, param, value0, value1, value2)
            VALUES (%s, %s, %s, %s, %s)""", (championship_id, parameter, points_list[0], points_list[1], points_list[2]))

    db.conn.commit()
