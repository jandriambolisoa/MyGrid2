import requests

from backend.config import settings as app_settings
from backend.db.database import get_db
from backend.src.drivers.dependencies import get_driver_registration_from_codename
from backend.src.live import signals as live_signals
from backend.src.results.router import override_session_results
from backend.src.users.schemas import UserSelf
from backend.src.events.constants import CHAMPIONSHIP_POINTS

async def update_session_results_from_live_session(session_id: int, user: UserSelf):
    db = get_db()
    db.cursor.execute("""
        SELECT championships.id AS championship_id
        FROM sessions
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE sessions.id = %s""", (session_id,))
    championship = db.cursor.fetchone()

    session_results = requests.get(f"{app_settings.ms_openf1_url}/results")
    datas = session_results.json()
    results = []

    for data in datas:
        driver = await get_driver_registration_from_codename(session_id, data.driver.codename)

        results.append({
            "driver_id": driver.driver.id,
            "results": data["position"],
            "points": CHAMPIONSHIP_POINTS[championship.id][data["position"]]
        })

    await override_session_results(results, session_id, "en", db, user)

    # Stop OpenF1 microservice
    requests.get(f"{app_settings.ms_openf1_url}/deactivate")


async def stop_openf1_microservice():
    # Stop OpenF1 microservice
    requests.get(f"{app_settings.ms_openf1_url}/deactivate")


def init_listener():
    # live_signals.closed.connect(update_session_results_from_live_session)
    live_signals.closed.connect(stop_openf1_microservice())

