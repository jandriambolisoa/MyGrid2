import asyncio
from datetime import datetime, UTC, timedelta

from apscheduler.jobstores.base import JobLookupError

from backend.db.database import get_db
from backend.scheduler import scheduler
from backend.src.collectibles.conditions import multiple_drivers_perfect_prediction
from backend.src.collectibles.dependencies import distribute_collectible
from backend.src.results.signals import updated_session_results


def distribute_multiple_drivers_perfect_prediction_rewards(session_id: int, *args):
    db = get_db()
    db.cursor.execute(""" \
        SELECT collectible_id, drivers_id
        FROM coll_multiple_drivers_perfect_prediction""")
    to_distribute = db.cursor.fetchall()

    for datas in to_distribute:
        # Get users that match the condition
        users = asyncio.run(multiple_drivers_perfect_prediction(session_id, datas["drivers_id"]))

        # Distribute a collectible to each one
        for user in users:
            asyncio.run(distribute_collectible(user.id, datas["collectible_id"]))

async def schedule_multiple_drivers_perfect_prediction_rewards_distribution(session_id: int, *args, **kwargs):
    try:
        scheduler.remove_job(f"distrib_collectibles_{session_id}")
    except JobLookupError:
        pass

    job_desc = f"Distribute after session collectibles - session_id:{session_id}"
    run_date = datetime.now(UTC) + timedelta(hours=6)

    scheduler.add_job(
        distribute_multiple_drivers_perfect_prediction_rewards,
        "date",
        run_date=run_date,
        args=[session_id,],
        id=f"distrib_collectibles_{session_id}",
        name=job_desc
    )

def init_listener():
    updated_session_results.connect(schedule_multiple_drivers_perfect_prediction_rewards_distribution)