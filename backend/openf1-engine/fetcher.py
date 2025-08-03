import ssl
import requests

import paho.mqtt.client as mqtt

from .config import settings

def get_access_token() -> str or None:
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
        access_token = login_response.json()["access_token"]
        return access_token
    else:
        return None

def fetch_session_type(access_token: str) -> str or None:
    """
    Returns the current session type.
    Returns:
        str: 'Practice', 'Qualifying' or 'Race'
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
        return session.json()["session_type"]
    else:
        return None

def fetch_drivers(access_token: str) -> list[dict] or None:
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

class LiveFetcher:

    datas: dict = dict()

    def __init__(self, session_type: str, access_token: str) -> None:
        """
        Setup MQTT connection and listen for incoming messages.
        Args:
            session_type: str, 'Practice', 'Qualifying' or 'Race'
            access_token: str, access token
        """
        self.access_token = access_token
        self.session_type = session_type

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(username=settings.openf1_api_username, password=access_token)
        self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS_CLIENT)

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        self.client.connect(settings.openf1_mqtt_broker, settings.openf1_mqtt_port, 60)
        self.client.loop_forever()  # Starts a blocking network loop

        print("# openf1-engine : Connected")

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0 and self.session_type == "Practice":
            client.subscribe("v1/position")
        if rc == 0 and self.session_type == "Qualifying":
            client.subscribe("v1/position")
            client.subscribe("v1/laps")
        if rc == 0 and self.session_type == "Race":
            client.subscribe("v1/position")
            client.subscribe("v1/intervals")
        else:
            print(f"# openf1-engine : Failed to connect, return code {rc}")

    def _on_message(self, client, userdata, msg):
        if msg.topic == "v1/position":
            for position in msg.payload.decode():
                self.datas[position["driver_number"]] = {"position": position["position"]}

        elif msg.topic == "v1/laps" and self.session_type == "Qualifying":
            for lap in msg.payload.decode():
                if "lap_duration" not in self.datas[lap["driver_number"]]:
                    self.datas[lap["driver_number"]]["lap_duration"] = lap["lap_duration"]
                elif self.datas[lap["driver_number"]]["lap_duration"] > lap["lap_duration"]:
                    self.datas[lap["driver_number"]]["lap_duration"] = lap["lap_duration"]
                else:
                    continue

        elif msg.topic == "v1/intervals" and self.session_type == "Race":
            for interval in msg.payload.decode():
                self.datas[interval["driver_number"]]["interval"] = interval["interval"]

        print(f"# openf1-engine : Received message on topic '{msg.topic}'")

    def get_datas(self):
        """
        Return last updated datas.
        Returns:
            dict: last updated datas. Format :
            {
                int (driver_number): {
                    'position': position,
                    'lap_duration': lap_duration,
                    'interval': interval
                }
            }
        """
        return self.datas

    def disconnect(self):
        """
        Disconnect MQTT client and return last updated datas.
        Returns:
            dict: last updated datas.
        """
        self.client.disconnect()
        return self.get_datas()
