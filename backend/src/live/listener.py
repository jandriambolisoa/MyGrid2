from datetime import datetime, timedelta

from backend.db.database import get_db
from backend.src.events.signals import create_session, delete_session
from backend.src.events.schemas import Session
from backend.src.live.constants import LIVE_SESSION_OPEN_DELTA, LIVE_SESSION_CLOSE_DELTA
from backend.src.live.router import open_live_session, close_live_session
from backend.src.users.schemas import UserSelf

from backend.scheduler import scheduler

async def schedule_live_session(session: Session, user: UserSelf):

    db = get_db()
    # Schedule this only if the championship id is 1
    db.cursor.execute("""
        SELECT championships.id AS championship_id
        FROM sessions
        LEFT JOIN events ON events.id = sessions.event_id
        LEFT JOIN championships ON championships.id = events.championship_id
        WHERE sessions.id = %s AND championships.id = %s""", (session.id, 1))
    championship = db.cursor.fetchone()

    if championship is None:
        return

    db.cursor.execute("""
        SELECT events.name
        FROM events
        WHERE events.id = %s""", (session.event_id,))
    event = db.cursor.fetchone()

    # Schedule open and close session

    if not event:
        job_desc_open = f"Open live session - id:{session.id} - user_id:{user.id} username:{user.username}"
        job_desc_close = f"Close live session - id:{session.id} - user_id:{user.id} username:{user.username}"
    else:
        job_desc_open = f"Open live session -  id:{session.id} name:{event['name']} {session.name} - user_id:{user.id} username:{user.username}"
        job_desc_close = f"Close live session -  id:{session.id} name:{event['name']} {session.name} - user_id:{user.id} username:{user.username}"

    run_date_open = session.datetime + timedelta(minutes=LIVE_SESSION_OPEN_DELTA)
    run_date_close = session.datetime + timedelta(minutes=LIVE_SESSION_CLOSE_DELTA)

    scheduler.add_job(
        open_live_session,
        "date",
        run_date=run_date_open,
        args=[session.id, "en", user],
        id=f"livesession_open_{session.id}",
        name=job_desc_open
    )
    scheduler.add_job(
        close_live_session,
        "date",
        run_date=run_date_close,
        args=["en", user],
        id=f"livesession_close_{session.id}",
        name=job_desc_close
    )

async def unschedule_live_session(session: Session, user: UserSelf):
    jobs_id = [f"livesession_open_{session.id}", f"livesession_close_{session.id}"]

    for job_id in jobs_id:
        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)

def init_listener():
    create_session.connect(schedule_live_session)
    delete_session.connect(unschedule_live_session)
