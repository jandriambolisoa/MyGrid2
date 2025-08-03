from datetime import datetime
from datetime import UTC

import requests

from .config import (
    OPENF1_API_URL,
    OPENF1_API_EP_DRIVERS,
    OPENF1_API_EP_INTERVALS,
    OPENF1_API_EP_LAPS,
    OPENF1_API_EP_POSITION,
    OPENF1_API_EP_SESSIONS
)

def fetch_session_type() -> str:
    """
    Returns the current session type.
    Returns:
        str: 'Practice', 'Qualifying' or 'Race'
    """
    params = {
        "session_key": "latest"
    }
    session = requests.get(
        OPENF1_API_URL+OPENF1_API_EP_SESSIONS,
        params=params
    )
    return session.json()["session_type"]

def fetch_drivers() -> list[dict]:
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
        JSON response as a list of dictionaries.
    """
    params = {
        "session_key": "latest"
    }
    drivers = requests.get(
        OPENF1_API_EP_DRIVERS+OPENF1_API_EP_DRIVERS,
        params=params,
    )
    return drivers.json()

def fetch_live_datas(race: bool = True):
    """
    Returns live datas for the current session.
    Datas format depends on session type.
    If race, returns for each driver its position
    and the interval to the next driver (or null for
    leader):
    [
      {
        "driver_number": 1,
        "position": 1,
        "interval": null,
      }
    ]
    If not race, returns for each driver its position
    and its fastest lap of the session:
    [
      {
        "driver_number": 1,
        "position": 1,
        "lap_duration": 92.365,
      }
    ]
    Args:
        race: bool

    Returns:
        JSON response as a list of dictionaries.
    """
    curr_datetime = datetime.now(UTC)
    params = {
        "session_key": "latest",
        "date": curr_datetime.isoformat()
    }
    positions = requests.get(
        OPENF1_API_URL+OPENF1_API_EP_POSITION,
        params=params
    )
    datas = dict()
    for p in positions.json():
        datas[p["driver_number"]] = {"position": p["position"]}

    if race:
        intervals = requests.get(
            OPENF1_API_URL+OPENF1_API_EP_INTERVALS,
            params=params
        )
        for interval in intervals.json():
            datas[interval["driver_number"]]["interval"] = interval["interval"]

    else:
        del params["date"]
        laps = requests.get(
            OPENF1_API_URL + OPENF1_API_EP_LAPS,
            params=params
        )
        for lap in laps.json():
            if "lap_duration" not in datas[lap["driver_number"]]:
                datas[lap["driver_number"]]["lap_duration"] = lap["lap_duration"]
            elif datas[lap["driver_number"]]["lap_duration"] > lap["lap_duration"]:
                datas[lap["driver_number"]]["lap_duration"] = lap["lap_duration"]
            else:
                continue

    return datas
