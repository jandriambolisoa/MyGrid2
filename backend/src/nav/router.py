from fastapi import APIRouter, Depends, status

from backend.constants import QUERY_LIMIT
from backend.db.database import Database, get_db
from backend.oauth2 import get_current_user
from backend.src.events.dependencies import valid_championship_id, get_upcoming_event,\
    is_session_over, get_event_championship
from backend.src.nav.exceptions import ChampionshipLeaderboardNotAvailableError
from backend.src.nav.schemas import NavMainEvent, NavMainEventSession, NavChampionship, NavChampionshipEvents, \
    DriverChampionshipLeaderboardWithPrediction, TeamChampionshipLeaderboardWithPrediction
from backend.src.predictions.dependencies import is_user_has_prono, get_user_wdc_prediction, get_user_wcc_prediction
from backend.src.ranks.schemas import ChampionshipRanks
from backend.src.users.schemas import UserSelf
from backend.utils import get_nice_datetime

router = APIRouter(
    prefix="/nav",
    tags= ["nav"]
)

#
# CRUD operations
#

@router.get("/home/main-event", response_model=NavMainEvent, status_code=status.HTTP_200_OK)
async def home_get_main_event(championship_id: int = Depends(valid_championship_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    event = await get_upcoming_event(language)
    championship = await get_event_championship(event.id, language)

    db.cursor.execute("""
        WITH sessions_translations AS (
            SELECT session_id, name
            FROM sessionstranslations
            WHERE language = %s
        )
        SELECT sessions.id,
        COALESCE(sessions_translations.name, sessions.name) AS name,
        sessions.datetime,
        sessions.competitive,
        sessions.event_id
        FROM sessions
        LEFT JOIN sessions_translations ON sessions_translations.session_id = sessions.id
        WHERE event_id = %s
        ORDER BY datetime ASC""", (language, event.id))
    sessions = db.cursor.fetchall()
    sessions_to_return = list()

    for session in sessions:
        has_prono = await is_user_has_prono(current_user.id, session["id"])
        nice_datetime= get_nice_datetime(session["datetime"], language)
        is_over= await is_session_over(session["id"])

        if is_over:
            db.cursor.execute("""\
                SELECT COALESCE(SUM(score), 0) AS total
                FROM scores
                WHERE user_id = %s
                AND session_id = %s""", (current_user.id, session["id"]))
            score_to_display = db.cursor.fetchone()
        else:
            db.cursor.execute("""\
                SELECT COALESCE(SUM(potential), 0) AS total
                FROM sessionspredictions
                WHERE user_id = %s
                AND session_id = %s""", (current_user.id, session["id"]))
            score_to_display = db.cursor.fetchone()

        session["has_prono"] = has_prono
        session["nice_datetime"] = nice_datetime
        session["is_over"] = is_over
        session["score"] = score_to_display["total"]

        sessions_to_return.append(NavMainEventSession(**session))

    return {
        "championship": championship,
        "event": event,
        "sessions": sessions_to_return
    }

@router.get("/home/championships", response_model=NavChampionship, status_code=status.HTTP_200_OK)
async def home_get_championships(championship_id: int = Depends(valid_championship_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    db.cursor.execute("""\
        SELECT * FROM championships
        WHERE id = %s""",(championship_id,))
    championship = db.cursor.fetchone()

    db.cursor.execute("""\
        WITH last_registrations AS (
            SELECT DISTINCT ON (sessionsregistrations.driver_id) sessionsregistrations.driver_id,
            teams.id AS team_id,
            teams.name AS team_name,
            teams.color AS team_color,
            sessions.datetime AS session_datetime
            FROM sessionsregistrations
            LEFT JOIN teams ON teams.id = sessionsregistrations.team_id
            LEFT JOIN sessions ON sessions.id = sessionsregistrations.session_id
            WHERE sessions.datetime < NOW()
            ORDER BY sessionsregistrations.driver_id, sessions.datetime DESC
        )
        SELECT drivers.id AS driver_id,
        drivers.firstname AS driver_firstname,
        drivers.lastname AS driver_lastname,
        drivers.codename AS driver_codename,
        last_registrations.team_id AS team_id,
        last_registrations.team_name AS team_name,
        last_registrations.team_color AS team_color,
        SUM(sessionsresults.points) AS score,
        ROW_NUMBER() OVER(ORDER BY SUM(sessionsresults.points) DESC) AS rank
        FROM sessionsresults
        LEFT JOIN drivers ON drivers.id = driver_id
        LEFT JOIN last_registrations ON last_registrations.driver_id = drivers.id
        LEFT JOIN sessions ON sessions.id = sessionsresults.session_id
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE championships.id = %s
        GROUP BY drivers.id, drivers.firstname, drivers.lastname, drivers.codename, last_registrations.team_id, last_registrations.team_name, last_registrations.team_color
        ORDER BY score DESC
        LIMIT 3""", (championship_id,))
    wdc_leaderboard = db.cursor.fetchall()

    db.cursor.execute("""\
        WITH drivers_teams AS (
            SELECT sessionsregistrations.session_id,
            sessionsregistrations.driver_id ,
            teams.id AS team_id,
            teams.name AS team_name,
            teams.color AS team_color
            FROM sessionsregistrations
            LEFT JOIN teams ON teams.id = sessionsregistrations.team_id
        )
        SELECT drivers_teams.team_id,
        drivers_teams.team_name,
        drivers_teams.team_color,
        SUM(sessionsresults.points) AS score,
        ROW_NUMBER() OVER(ORDER BY SUM(sessionsresults.points) DESC) AS rank
        FROM sessionsresults
        LEFT JOIN drivers_teams ON drivers_teams.session_id = sessionsresults.session_id AND drivers_teams.driver_id = sessionsresults.driver_id
        LEFT JOIN sessions ON sessions.id = sessionsresults.session_id
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE championships.id = %s
        GROUP BY drivers_teams.team_id, drivers_teams.team_name, drivers_teams.team_color
        ORDER BY score DESC""", (championship_id,))
    wcc_leaderboard = db.cursor.fetchone()

    db.cursor.execute("""\
        SELECT * FROM wdcpredictions
        WHERE championship_id = %s AND user_id = %s""", (championship_id, current_user.id))
    wdc_prono = db.cursor.fetchone()

    db.cursor.execute("""\
        SELECT * FROM wccpredictions
        WHERE championship_id = %s AND user_id = %s""", (championship_id, current_user.id))
    wcc_prono = db.cursor.fetchone()

    if not wcc_leaderboard or not wdc_leaderboard:
        ChampionshipLeaderboardNotAvailableError(language= language)

    # From here, convert queries results into dict
    ## DriverRank
    wdc_ranks = list()
    for driver_rank in wdc_leaderboard:
        driver = {key.removeprefix("driver_"): driver_rank[key] for key in driver_rank.keys() if key.startswith("driver_")}
        team = {key.removeprefix("team_"): driver_rank[key] for key in driver_rank.keys() if key.startswith("team_")}

        wdc_ranks.append({
            "rank": driver_rank["rank"],
            "driver": driver,
            "team": team,
            "score": driver_rank["score"]
        })

    ## TeamRank
    wcc_ranks = list()
    # for team_rank in wcc_leaderboard: # Query fetch a single entry
    team = {key.removeprefix("team_"): wcc_leaderboard[key] for key in wcc_leaderboard.keys() if key.startswith("team_")}

    wcc_ranks.append({
        "rank": wcc_leaderboard["rank"],
        "team": team,
        "score": wcc_leaderboard["score"]
    })

    return {
        "championship": {**championship},
        "wdc": {
            "leaderboard": {
                "championship": {**championship},
                "ranks": wdc_ranks
            },
            "has_prono": True if wdc_prono else False
        },
        "wcc": {
            "leaderboard": {
                "championship": {**championship},
                "ranks": wcc_ranks
            },
            "has_prono": True if wcc_prono else False
        }
    }

@router.get("/home/events", response_model=NavChampionshipEvents, status_code=status.HTTP_200_OK)
async def home_get_events(championship_id: int = Depends(valid_championship_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    db.cursor.execute("""\
        SELECT * FROM championships
        WHERE id = %s""",(championship_id,))
    championship = db.cursor.fetchone()

    db.cursor.execute("""\
        WITH events_translations AS (
            SELECT event_id, name
            FROM eventstranslations
            WHERE language = %s
        )
        SELECT DISTINCT ON (events.id) events.id AS event_id,
        COALESCE(events_translations.name, events.name) AS event_name,
        events.colors AS event_colors,
        events.championship_id AS event_championship_id,
        events.flag AS event_flag,
        sessions.datetime AS event_datetime
        FROM sessions
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN events_translations ON events_translations.event_id = events.id
        WHERE events.championship_id = %s AND sessions.competitive = true
        ORDER BY events.id, sessions.datetime DESC""", (language, championship_id))
    events = db.cursor.fetchall()

    return {
        "championship": {**championship},
        "events": sorted([
            {key.removeprefix("event_"): event[key] for key in event.keys() if key.startswith("event_")}
            for event in events
        ], key=lambda event: event["datetime"])
    }


@router.get("/standings/drivers", response_model=DriverChampionshipLeaderboardWithPrediction, status_code=status.HTTP_200_OK)
async def get_championship_drivers_standings(championship_id: int = Depends(valid_championship_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    db.cursor.execute("""\
        SELECT * FROM championships
        WHERE id = %s""", (championship_id,))
    championship = db.cursor.fetchone()

    db.cursor.execute("""\
        WITH last_registrations AS (
            SELECT DISTINCT ON (sessionsregistrations.driver_id) sessionsregistrations.driver_id,
            teams.id AS team_id,
            teams.name AS team_name,
            teams.color AS team_color
            FROM sessionsregistrations
            LEFT JOIN teams ON teams.id = sessionsregistrations.team_id
            WHERE session_id IN (
                SELECT sessions.id AS session_id
                FROM sessions
                WHERE sessions.datetime < NOW()
                ORDER BY datetime DESC
            )
        )
        SELECT drivers.id AS driver_id,
        drivers.firstname AS driver_firstname,
        drivers.lastname AS driver_lastname,
        drivers.codename AS driver_codename,
        last_registrations.team_id AS team_id,
        last_registrations.team_name AS team_name,
        last_registrations.team_color AS team_color,
        SUM(sessionsresults.points) AS score,
        ROW_NUMBER() OVER(ORDER BY SUM(sessionsresults.points) DESC) AS rank
        FROM sessionsresults
        LEFT JOIN drivers ON drivers.id = driver_id
        LEFT JOIN last_registrations ON last_registrations.driver_id = drivers.id
        LEFT JOIN sessions ON sessions.id = sessionsresults.session_id
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE championships.id = %s
        GROUP BY drivers.id, drivers.firstname, drivers.lastname, drivers.codename, last_registrations.team_id, last_registrations.team_name, last_registrations.team_color
        ORDER BY score DESC""", (championship_id,))
    wdc_leaderboard = db.cursor.fetchall()

    return {
        "championship": {**championship},
        "ranks":[{
            "rank": driver["rank"],
            "driver": {key.removeprefix("driver_"): driver[key] for key in driver.keys() if key.startswith("driver_")},
            "team": {key.removeprefix("team_"): driver[key] for key in driver.keys() if key.startswith("team_")},
            "score": driver["score"]
        } for driver in wdc_leaderboard],
        "driver_id_prediction": await get_user_wdc_prediction(current_user.id, championship_id)
    }


@router.get("/standings/teams", response_model=TeamChampionshipLeaderboardWithPrediction, status_code=status.HTTP_200_OK)
async def get_championship_teams_standings(championship_id: int = Depends(valid_championship_id), language: str = "en", db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    db.cursor.execute("""\
        SELECT * FROM championships
        WHERE id = %s""", (championship_id,))
    championship = db.cursor.fetchone()

    db.cursor.execute("""\
        WITH drivers_teams AS (
            SELECT sessionsregistrations.session_id,
            sessionsregistrations.driver_id ,
            teams.id AS team_id,
            teams.name AS team_name,
            teams.color AS team_color
            FROM sessionsregistrations
            LEFT JOIN teams ON teams.id = sessionsregistrations.team_id
        )
        SELECT drivers_teams.team_id,
        drivers_teams.team_name,
        drivers_teams.team_color,
        SUM(sessionsresults.points) AS score,
        ROW_NUMBER() OVER(ORDER BY SUM(sessionsresults.points) DESC) AS rank
        FROM sessionsresults
        LEFT JOIN drivers_teams ON drivers_teams.session_id = sessionsresults.session_id AND drivers_teams.driver_id = sessionsresults.driver_id
        LEFT JOIN sessions ON sessions.id = sessionsresults.session_id
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE championships.id = %s
        GROUP BY drivers_teams.team_id, drivers_teams.team_name, drivers_teams.team_color
        ORDER BY score DESC""", (championship_id,))
    wcc_leaderboard = db.cursor.fetchall()

    return {
        "championship": {**championship},
        "ranks":[{
            "rank": team["rank"],
            "team": {key.removeprefix("team_"): team[key] for key in team.keys() if key.startswith("team_")},
            "score": team["score"]
        } for team in wcc_leaderboard],
        "team_id_prediction": await get_user_wcc_prediction(current_user.id, championship_id)
    }
