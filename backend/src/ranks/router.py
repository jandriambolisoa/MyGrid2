from fastapi import APIRouter, Depends, status
from psycopg.errors import UniqueViolation, ForeignKeyViolation

from backend.constants import QUERY_LIMIT
from backend.db.database import Database, get_db
from backend import exceptions as app_exceptions
from backend.oauth2 import get_current_user
from backend.src.events.dependencies import valid_session_id, valid_championship_id, valid_event_id, get_last_event_id
from backend.src.ranks.constants import RANK_QUERY_LIMIT
from backend.src.ranks.exceptions import NoRanksError
from backend.src.ranks.schemas import ChampionshipRanks, EventRanks, SessionRanks
from backend.src.results.exceptions import NoResultsFoundError, InvalidSessionResultsAttemptError
from backend.src.results.schemas import ResultSession, ResultPost
from backend.src.users.privileges import is_user_moderator_or_admin
from backend.src.users.schemas import UserSelf
from backend.src.results import signals as results_signals

router = APIRouter(
    prefix="/ranks",
    tags= ["ranks"]
)

#
# CRUD operations
#

@router.get("/championships/{championship_id}", response_model=ChampionshipRanks)
async def get_championships_ranks(
        championship_id: int = Depends(valid_championship_id),
        language: str = "en",
        db: Database = Depends(get_db),
        current_user: UserSelf = Depends(get_current_user),
        limit: int = RANK_QUERY_LIMIT,
        page: int = 0):

    offset = limit * page

    db.cursor.execute("""
        SELECT users.id AS user_id,
        users.username AS user_username,
        users.created AS user_created,
        users.image AS user_image,
        ranks_championships_mv.rank AS rank,
        ranks_championships_mv.score AS score,
        championships.id AS championship_id,
        championships.name AS championship_name
        FROM ranks_championships_mv
        LEFT JOIN users ON users.id = ranks_championships_mv.user_id
        LEFT JOIN championships ON championships.id = ranks_championships_mv.championship_id
        WHERE ranks_championships_mv.championship_id = %s
        ORDER BY ranks_championships_mv.rank ASC
        LIMIT %s OFFSET %s""", (championship_id, limit, offset))

    ranks = db.cursor.fetchall()

    if not ranks:
        raise NoRanksError(language=language)

    # Get current user rank
    db.cursor.execute("""
        SELECT users.id AS user_id,
        users.username AS user_username,
        users.created AS user_created,
        users.image AS user_image,
        ranks_championships_mv.rank AS rank,
        ranks_championships_mv.score AS score
        FROM ranks_championships_mv
        LEFT JOIN users ON users.id = ranks_championships_mv.user_id
        WHERE ranks_championships_mv.championship_id = %s AND users.id = %s""", (championship_id, current_user.id))

    current_user_rank = db.cursor.fetchone()

    ranks_result = list()
    # Convert query result into UserRank schema
    for rank in ranks:
        user = {key.removeprefix("user_"): rank[key] for key in rank.keys() if key.startswith("user_")}

        ranks_result.append({
            "rank": rank["rank"],
            "user": user,
            "score": rank["score"]
        })

    viewer_rank = {
        "rank": current_user_rank["rank"] if current_user_rank else None,
        "user": {key.removeprefix("user_"): current_user_rank[key] for key in current_user_rank.keys() if key.startswith("user_")} if current_user_rank else None,
        "score": current_user_rank["score"] if current_user_rank else None
    }

    return {
        "championship": {key.removeprefix("championship_"): ranks[0][key] for key in ranks[0].keys() if key.startswith("championship_")},
        "viewer_rank": viewer_rank,
        "ranks": ranks_result
    }


@router.get("/events", response_model=EventRanks)
async def get_events_ranks(
        event_id: int = Depends(get_last_event_id),
        language: str = "en",
        db: Database = Depends(get_db),
        current_user: UserSelf = Depends(get_current_user),
        limit: int = RANK_QUERY_LIMIT,
        page: int = 0):

    offset = limit * page

    db.cursor.execute("""
        WITH events_translations AS (
            SELECT event_id, name
            FROM eventstranslations
            WHERE language = %s
        )
        SELECT users.id AS user_id,
        users.username AS user_username,
        users.created AS user_created,
        users.image AS user_image,
        ranks_events_mv.rank AS rank,
        ranks_events_mv.score AS score,
        championships.id AS championship_id,
        championships.name AS championship_name,
        events.id AS event_id,
        COALESCE(events_translations.name, events.name) AS event_name,
        events.championship_id AS event_championship_id,
        events.colors AS event_colors,
        events.flag AS event_flag
        FROM ranks_events_mv
        LEFT JOIN users ON users.id = ranks_events_mv.user_id
        LEFT JOIN championships ON championships.id = ranks_events_mv.championship_id
        LEFT JOIN events ON events.id = ranks_events_mv.event_id
        LEFT JOIN events_translations ON events_translations.event_id = ranks_events_mv.event_id
        WHERE ranks_events_mv.event_id = %s
        ORDER BY ranks_events_mv.rank ASC
        LIMIT %s OFFSET %s""", (language, event_id, limit, offset))

    ranks = db.cursor.fetchall()

    if not ranks:
        raise NoRanksError(language=language)

    # Get current user rank
    db.cursor.execute("""
        SELECT users.id AS user_id,
        users.username AS user_username,
        users.created AS user_created,
        users.image AS user_image,
        ranks_events_mv.rank AS rank,
        ranks_events_mv.score AS score
        FROM ranks_events_mv
        LEFT JOIN users ON users.id = ranks_events_mv.user_id
        WHERE ranks_events_mv.event_id = %s AND users.id = %s""", (event_id, current_user.id))

    current_user_rank = db.cursor.fetchone()

    ranks_result = list()
    # Convert query result into UserRank schema
    for rank in ranks:
        user = {key.removeprefix("user_"): rank[key] for key in rank.keys() if key.startswith("user_")}

        ranks_result.append({
            "rank": rank["rank"],
            "user": user,
            "score": rank["score"]
        })

    viewer_rank = {
        "rank": current_user_rank["rank"] if current_user_rank else None,
        "user": {key.removeprefix("user_"): current_user_rank[key] for key in current_user_rank.keys() if key.startswith("user_")} if current_user_rank else None,
        "score": current_user_rank["score"] if current_user_rank else None
    }

    return {
        "championship": {key.removeprefix("championship_"): ranks[0][key] for key in ranks[0].keys() if key.startswith("championship_")},
        "event": {key.removeprefix("event_"): ranks[0][key] for key in ranks[0].keys() if key.startswith("event_")},
        "viewer_rank": viewer_rank,
        "ranks": ranks_result
    }


@router.get("/records/sessions/{championship_id}", response_model=SessionRanks)
async def get_records_sessions_ranks(
        championship_id: int = Depends(valid_championship_id),
        language: str = "en",
        db: Database = Depends(get_db),
        current_user: UserSelf = Depends(get_current_user),
        limit: int = RANK_QUERY_LIMIT,
        page: int = 0):

    offset = limit * page

    db.cursor.execute("""
        WITH events_translations AS (
            SELECT event_id, name
            FROM eventstranslations
            WHERE language = %s
        ),
        sessions_translations AS (
            SELECT session_id, name
            FROM sessionstranslations
            WHERE language = %s
        )
        SELECT users.id AS user_id,
        users.username AS user_username,
        users.created AS user_created,
        users.image AS user_image,
        ranks_sessions_mv.rank AS rank,
        ranks_sessions_mv.score AS score,
        championships.id AS championship_id,
        championships.name AS championship_name,
        events.id AS event_id,
        COALESCE(events_translations.name, events.name) AS event_name,
        events.championship_id AS event_championship_id,
        events.colors AS event_colors,
        events.flag AS event_flag,
        sessions.id AS session_id,
        COALESCE(sessions_translations.name, sessions.name) AS session_name,
        sessions.datetime AS session_datetime,
        sessions.event_id AS session_event_id,
        sessions.competitive AS session_competitive    
        FROM ranks_sessions_mv
        LEFT JOIN users ON users.id = ranks_sessions_mv.user_id
        LEFT JOIN championships ON championships.id = ranks_sessions_mv.championship_id
        LEFT JOIN sessions ON sessions.id = ranks_sessions_mv.session_id
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN sessions_translations ON sessions_translations.session_id = ranks_sessions_mv.session_id
        LEFT JOIN events_translations ON events_translations.event_id = sessions.event_id
        WHERE ranks_sessions_mv.championship_id = %s
        ORDER BY ranks_sessions_mv.rank ASC
        LIMIT %s OFFSET %s""", (language, language, championship_id, limit, offset))

    ranks = db.cursor.fetchall()

    if not ranks:
        raise NoRanksError(language=language)

    ranks_result = list()
    # Convert query result into UserRank schema
    for rank in ranks:
        user = {key.removeprefix("user_"): rank[key] for key in rank.keys() if key.startswith("user_")}
        event = {key.removeprefix("event_"): rank[key] for key in rank.keys() if key.startswith("event_")}
        session = {key.removeprefix("session_"): rank[key] for key in rank.keys() if key.startswith("session_")}

        ranks_result.append({
            "rank": rank["rank"],
            "user": user,
            "event": event,
            "session": session,
            "score": rank["score"]
        })

    return {
        "championship": {key.removeprefix("championship_"): ranks[0][key] for key in ranks[0].keys() if key.startswith("championship_")},
        "ranks": ranks_result
    }
