import asyncio
import requests

from fastapi import WebSocket

from backend.config import settings as app_settings
from backend.src.drivers.dependencies import get_driver_registration_from_codename
from backend.src.live.constants import WEBSOCKET_COOLDOWN_SECONDS


class LiveSession:

    instance = None

    def __init__(self, session_id: int):
        self.users_ws = {}
        self.session_id = session_id

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.users_ws["user%07d" % user_id] = websocket

    def disconnect(self, user_id: int):
        del self.users_ws["user%07d" %int(user_id)]

    def disconnect_all(self):
        del self.users_ws

    async def send(self, datas: list):
        for user_id in self.users_ws:
            await self.users_ws[user_id].send_json(datas)


def get_live_session(session_id: int = None) -> LiveSession | None:
    """
    Returns a LiveSession instance. If no args, returns the instance or None if no instance.
    :param session_id: (int) the live session id from MyGrid database
    :return: :class:`LiveSession` a class instance
    """
    if not session_id:
        return LiveSession.instance
    if not LiveSession.instance:
        LiveSession.instance = LiveSession(session_id)
    elif session_id != LiveSession.instance.session_id:
        LiveSession.instance = LiveSession(session_id)
    return LiveSession.instance


async def engine(live_session: LiveSession):
    """
    Run an engine that will send session datas regularly to the websockets until session results are out.
    :args: :class:`LiveSession` instance
    :return: None
    """
    while True:
        try:
            # Get datas
            response = requests.get(f"{app_settings.ms_openf1_url}/datas")
            to_send = list()
            for data in response.json():
                driver = await get_driver_registration_from_codename(live_session.session_id, data["driver"]["codename"])
                to_send.append({
                    "position": data["position"],
                    "lap_duration": data["lap_duration"],
                    "interval": data["interval"],
                    "driver": driver.driver.model_dump(mode="json"),
                    "team": driver.team.model_dump(mode="json"),
                    "prediction": driver.prediction
                })

            # Send them to the websocket
            await live_session.send(to_send)

            # Cooldown
            await asyncio.sleep(WEBSOCKET_COOLDOWN_SECONDS)

        except Exception as error:
            break

        # # Get session results
        # session_results = requests.get(f"{app_settings.ms_openf1_url}/results")
        #
        # if session_results.status_code == 200:
        #     print("# DEBUG - results - %s"%session_results.json())
        #     if not session_results.json():
        #         continue
        #     to_send.clear()
        #     for data in session_results.json():
        #         driver = await get_driver_registration_from_codename(live_session.session_id, data["driver"]["codename"])
        #         to_send.append({
        #             "position": data["position"],
        #             "lap_duration": data["lap_duration"],
        #             "interval": data["interval"],
        #             "driver": driver.driver,
        #             "team": driver.team,
        #             "prediction": driver.prediction
        #         })
        #     await live_session.send(to_send)
