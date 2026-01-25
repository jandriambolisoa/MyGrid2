import asyncio
from datetime import datetime, UTC
from typing import Union

import requests
from fastapi import APIRouter, Depends, status
from starlette.websockets import WebSocket, WebSocketDisconnect

from backend.config import settings as app_settings
from backend.db.database import Database, get_db
from backend.exceptions import MicroservicesAreOffException
from backend.oauth2 import get_current_user
from backend import exceptions as app_exceptions
from backend.src.live.core import get_live_session, engine
from backend.src.live.exceptions import OpenF1MicroserviceError, NoLiveSessionError
from backend.src.live import signals as live_signals
from backend.src.live.signals import closed
from backend.src.users.privileges import is_user_moderator_or_admin
from backend.src.users.schemas import UserSelf
from backend.scheduler import scheduler
from backend.schemas import ScheduledJob

router = APIRouter(
    prefix="/live",
    tags= ["live"]
)

#
# CRUD operations
#
@router.get("/scheduler", response_model=list[ScheduledJob])
async def get_scheduled_live_sessions(current_user: UserSelf = Depends(get_current_user)):
    jobs = scheduler.get_jobs()

    return [
        {"id": job.id, "name": job.name, "datetime": job.next_run_time.isoformat()} for job in jobs if job.id.startswith("livesession_") and job.next_run_time > datetime.now(UTC)
    ]


#
# Websocket and live sessions
#
@router.websocket("/f1/ws")
async def listen_to_f1(
        token: str,
        websocket: WebSocket,
        language: str = "en",
        db:Database = Depends(get_db)):
    current_user = await get_current_user(token, db)

    live_session = get_live_session()

    if not live_session or not live_session.session_id:
        raise NoLiveSessionError(language=language)

    await live_session.connect(current_user.id, websocket)

    try:
        while True:
            await websocket.receive_json()

    except WebSocketDisconnect:
        live_session.disconnect(current_user.id)

    except RuntimeError as error:
        live_session.disconnect(current_user.id)


@router.get("/f1/open_session")
def open_live_session(session_id: int, language: str = "en", current_user: UserSelf = Depends(get_current_user)):
    if not asyncio.run(is_user_moderator_or_admin(current_user.id)):
        app_exceptions.forbidden_access_message(language)

    if app_settings.ms == 0:
        raise MicroservicesAreOffException(language=language)

    # Run OpenF1 microservice
    activation = requests.get(f"{app_settings.ms_openf1_url}/activate")
    if activation.status_code != 200:
        raise OpenF1MicroserviceError(language=language)

    live_session = get_live_session(session_id)

    try:
        asyncio.run(engine(live_session))
    except OpenF1MicroserviceError:
        live_signals.error.send()


@router.get("/f1/close_session")
def close_live_session(language: str = "en", current_user: UserSelf = Depends(get_current_user)):
    if not asyncio.run(is_user_moderator_or_admin(current_user.id)):
        app_exceptions.forbidden_access_message(language)

    live_session = get_live_session()

    if live_session:
        live_session.disconnect_all()

        closed.send(live_session.session_id, user=current_user) # OpenF1 microservice is stopped here
        live_session.session_id = None
        del live_session.instance
