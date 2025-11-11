import json
import ssl
import requests
import time

import paho.mqtt.client as mqtt

from backend.openf1.config import settings
from backend.openf1 import exceptions as openf1_exceptions
from backend.openf1.schemas import Driver, DriverLive


def get_access_token(language: str = "en") -> str or None:
    """
    Returns access token with MyGrid credentials
    Returns:
        str or None: None if the login failed
    """
    payload = {
        "username": settings.openf1_api_username,
        "password": settings.openf1_api_password
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    login_response = requests.post(
        settings.openf1_token_url,
        data=payload,
        headers=headers
    )

    if login_response.status_code == 200:
        access_token = login_response.json()
        return access_token["access_token"]
    else:
        raise openf1_exceptions.OpenF1CannotGetAccessTokenException(language=language)

def get_session(access_token: str) -> dict or None:
    """
    Returns the current session.
    Returns:
        dict: {"session_type": str, "session_key": str}
        None: None if the authentification failed
    """
    params = {
        "session_key": "latest"
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    session = requests.get(
        settings.openf1_api_url+"v1/sessions",
        params=params,
        headers=headers
    )

    if session.status_code == 200:
        session_datas = session.json()
        return {
            "session_type": session_datas[0]["session_type"],
            "session_key": session_datas[0]["session_key"]
        }
    else:
        return None

def get_results(access_token: str, session_key: int, drivers: list[Driver]) -> dict or None:
    params = {
        "session_key": "latest"
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(
        settings.openf1_api_url+"v1/session_result",
        params=params,
        headers=headers
    )

    if response.status_code == 200:
        driver_number_to_codename = {driver["driver_number"]: driver["name_acronym"] for driver in drivers}

        results_datas = response.json()
        if results_datas[0]["session_key"] == session_key:
            results = list()
            for result in results_datas:
                results.append({
                    "position": result["position"],
                    "lap_duration": None,
                    "interval": None,
                    "driver": {
                        "number": result["driver_number"],
                        "codename": driver_number_to_codename[result["driver_number"]]
                    }
                })
            return results
        else:
            return None
    else:
        return None

def get_drivers(access_token: str) -> list[dict] or None:
    """
    Returns the list of registered drivers for
    the current session. Format:
    [
      {
        "broadcast_name": "M VERSTAPPEN",
        "country_code": "NED",
        "driver_number": 1,
        "first_name": "Max",
        "full_name": "Max VERSTAPPEN",
        "headshot_url": "https://www.formula1.com/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/1col/image.png",
        "last_name": "Verstappen",
        "meeting_key": 1219,
        "name_acronym": "VER",
        "session_key": 9158,
        "team_colour": "3671C6",
        "team_name": "Red Bull Racing"
      }
    ]
    Returns:
        list[dict]: registered drivers
        None: None if the authentification failed
    """
    params = {
        "session_key": "latest"
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    drivers = requests.get(
        settings.openf1_api_url+"v1/drivers",
        params=params,
        headers=headers
    )

    if drivers.status_code == 200:
        return drivers.json()
    else:
        return None


class Leaderboard:

    def __init__(self):
        """
        Datas are received in this dict format:
        {
            int (driver_number): {
                'position': position,
                'lap_duration': lap_duration,
                'interval': interval
            }
        }
        """
        self.datas = dict()

    def read(self, drivers: list[Driver]):
        """
        Returns sorted datas as a list of DriverLive models.
        :param drivers: list of Driver models
        :return: list of DriverLive
        """
        driver_number_to_codename = {driver["driver_number"]: driver["name_acronym"] for driver in drivers}
        sorted_datas = []

        for driver_number in self.datas.keys():
            if self.datas[driver_number]["lap_duration"]:
                seconds = self.datas[driver_number]["lap_duration"]
                minutes = int(seconds/60)
                seconds = "%.3f" %(seconds-(minutes*60))
                laptime = f"{minutes}:{seconds}"
            else:
                laptime = self.datas[driver_number]["lap_duration"]

            sorted_datas.append(DriverLive(
                position=self.datas[driver_number]["position"],
                lap_duration=laptime,
                interval=self.datas[driver_number]["interval"],
                driver=Driver(
                    number=driver_number,
                    codename=driver_number_to_codename[driver_number]
                )
            ))

        sorted_datas.sort(key=lambda x: x.position)
        return sorted_datas

    def reset(self):
        self.datas.clear()

leaderboard = Leaderboard()

def on_connect(client, userdata, flags, rc, properties=None):
    # Get session initial positions
    number_of_drivers = len(userdata["drivers"])
    api_url = f"{settings.openf1_api_url}v1/position?session_key=latest"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {userdata['access_token']}"
    }

    for driver in userdata["drivers"]:
        response = requests.get(f"{api_url}&driver_number={driver['driver_number']}", headers=headers)
        if response.status_code == 200:
            raw_datas = response.json()
            last_position = raw_datas[-1]["position"]
            leaderboard.datas[driver["driver_number"]] = {
                "position": last_position,
                "lap_duration": None,
                "interval": None
            }

    # Subscribe to message types
    try:
        if rc == 0 and userdata["session_type"] == "Practice":
            client.subscribe("v1/position")
        if rc == 0 and userdata["session_type"] == "Qualifying":
            client.subscribe("v1/position")
            client.subscribe("v1/laps")
        if rc == 0 and userdata["session_type"] == "Race":
            client.subscribe("v1/position")
            client.subscribe("v1/intervals")
    except Exception as e:
        print(e)
    # else:
    #     raise openf1_exceptions.OpenF1ConnectionFailed() #TODO: logs system

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf8'))

    if msg.topic == "v1/position":
        leaderboard.datas[data["driver_number"]]["position"] = data["position"]

    elif msg.topic == "v1/laps" and data["lap_duration"]:
        if leaderboard.datas[data["driver_number"]]["lap_duration"] == None:
            leaderboard.datas[data["driver_number"]]["lap_duration"] = data["lap_duration"]
        elif leaderboard.datas[data["driver_number"]]["lap_duration"] > data["lap_duration"]:
            leaderboard.datas[data["driver_number"]]["lap_duration"] = data["lap_duration"]

    elif msg.topic == "v1/intervals":
        leaderboard.datas[data["driver_number"]]["interval"] = data["interval"]

def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    pass
