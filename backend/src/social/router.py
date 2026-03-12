from fastapi import APIRouter, Depends, status

from backend.constants import QUERY_LIMIT
from backend.db.database import Database, get_db
from backend.oauth2 import get_current_user
from backend.src.events.dependencies import valid_championship_id, get_upcoming_event, \
    is_session_over, get_event_championship, get_last_event_id, get_event_from_id, get_championship_from_id, \
    get_session_from_id
from backend.src.nav.exceptions import ChampionshipLeaderboardNotAvailableError
from backend.src.nav.schemas import NavMainEvent, NavMainEventSession, NavChampionship, NavChampionshipEvents, \
    DriverChampionshipLeaderboardWithPrediction, TeamChampionshipLeaderboardWithPrediction
from backend.src.predictions.dependencies import is_user_has_prono, get_user_wdc_prediction, get_user_wcc_prediction
from backend.src.ranks.exceptions import NoRanksError
from backend.src.ranks.schemas import ChampionshipRanks, UserEventRank, UserChampionshipRank, UserSessionRank
from backend.src.users.dependencies import get_current_user_language
from backend.src.users.schemas import UserSelf
from backend.utils import get_nice_datetime

router = APIRouter(
    prefix="/nav/social",
    tags= ["nav"]
)

#
# CRUD operations
#

@router.get("/home/event-rank", response_model=UserEventRank, status_code=status.HTTP_200_OK)
async def get_social_event_rank(
        event_id: int = Depends(get_last_event_id),
        language: str = Depends(get_current_user_language),
        db: Database = Depends(get_db),
        current_user: UserSelf = Depends(get_current_user)):

    db.cursor.execute("""\
        SELECT ranks_events_mv.rank, 
        ranks_events_mv.event_id,
        ranks_events_mv.score
        FROM ranks_events_mv
        WHERE ranks_events_mv.user_id = %s
        AND ranks_events_mv.event_id = %s
        """, (current_user.id, event_id))
    rank = db.cursor.fetchone()

    if not rank:
        return {
            "rank": -1,
            "user": current_user,
            "event": await get_event_from_id(event_id, language=language)
        }

    return {
        "rank": rank["rank"],
        "user": current_user,
        "event": await get_event_from_id(event_id, language=language),
        "score": rank["score"]
    }

@router.get("/home/championship-rank", response_model=UserChampionshipRank, status_code=status.HTTP_200_OK)
async def get_social_championship_rank(
        championship_id: int = Depends(valid_championship_id),
        language: str = Depends(get_current_user_language),
        db: Database = Depends(get_db),
        current_user: UserSelf = Depends(get_current_user)):

    db.cursor.execute("""\
        SELECT ranks_championships_mv.rank,
        ranks_championships_mv.championship_id,
        ranks_championships_mv.score
        FROM ranks_championships_mv
        WHERE ranks_championships_mv.user_id = %s
        AND ranks_championships_mv.championship_id = %s
        """, (current_user.id, championship_id))
    rank = db.cursor.fetchone()

    if not rank:
        return {
            "rank": -1,
            "user": current_user,
            "championship": await get_championship_from_id(championship_id, language=language)
        }

    return {
        "rank": rank["rank"],
        "user": current_user,
        "championship": await get_championship_from_id(championship_id, language=language),
        "score": rank["score"]
    }

@router.get("/home/session-rank", response_model=UserSessionRank, status_code=status.HTTP_200_OK)
async def get_social_session_rank(
        championship_id: int = Depends(valid_championship_id),
        language: str = Depends(get_current_user_language),
        db: Database = Depends(get_db),
        current_user: UserSelf = Depends(get_current_user)):

    db.cursor.execute("""\
        SELECT ranks_sessions_mv.rank,
        ranks_sessions_mv.championship_id,
        ranks_sessions_mv.session_id,
        ranks_sessions_mv.score
        FROM ranks_sessions_mv
        WHERE ranks_sessions_mv.user_id = %s
        AND ranks_sessions_mv.championship_id = %s
        ORDER BY rank ASC
        """, (current_user.id, championship_id))
    rank = db.cursor.fetchone()

    if not rank:
        raise NoRanksError(language)

    session = await get_session_from_id(rank["session_id"], language=language)
    event = await get_event_from_id(session.id, language=language)

    return {
        "rank": rank["rank"],
        "user": current_user,
        "event": event,
        "session": session,
        "score": rank["score"]
    }
