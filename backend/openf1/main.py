import ssl

from backend.openf1.config import settings
from backend.openf1.dependencies import (
    get_access_token,
    get_drivers,
    get_session,
    on_connect, on_message, leaderboard, get_results,
)

from fastapi import FastAPI, Depends, status, Response
from fastapi.middleware.cors import CORSMiddleware

import paho.mqtt.client as mqtt

from backend.openf1.schemas import DriverLive

docs_urls = {
    "docs_url": "/docs" if settings.debug else None,
    "redoc_url": "/redoc" if settings.debug else None,
    "openapi_url": "/openapi.json" if settings.debug else None,
}
app = FastAPI(**docs_urls)

# Init middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_openf1_client(access_token: str):
    cli = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    cli.username_pw_set(username=settings.openf1_api_username, password=access_token)
    cli.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS_CLIENT)
    session = get_session(access_token)
    client_datas = {
        "access_token": access_token,
        "session_type": session["session_type"],
        "session_key": session["session_key"],
        "drivers": get_drivers(access_token)
    }
    cli.user_data_set(client_datas)

    return cli

access_token = get_access_token()
client = get_openf1_client(access_token)

@app.get("/activate")
async def activate():
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(settings.openf1_mqtt_broker, settings.openf1_mqtt_port, 60)
    client.loop_start()


@app.get("/deactivate")
async def deactivate():
    client.disconnect()
    leaderboard.reset()


@app.get("/datas", response_model=list[DriverLive])
async def datas():
    return leaderboard.read(client.user_data_get()["drivers"])


@app.get("/results", response_model=list[DriverLive])
async def results():
    return get_results(
        access_token,
        client.user_data_get()["session_key"],
        client.user_data_get()["drivers"]
    ) if not None else Response(status_code=status.HTTP_204_NO_CONTENT)
