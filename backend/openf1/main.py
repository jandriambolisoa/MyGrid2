import ssl

from backend.openf1.config import settings
from backend.openf1.dependencies import (
    on_connect, on_message, leaderboard, get_openf1_client, OpenF1Interface
)

from fastapi import FastAPI, Depends, status, Response
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/activate")
async def activate():
    cli = get_openf1_client()

    cli.on_connect = on_connect
    cli.on_message = on_message

    cli.connect(settings.openf1_mqtt_broker, settings.openf1_mqtt_port, 60)
    cli.loop_start()


@app.get("/deactivate")
async def deactivate():
    cli = get_openf1_client()
    cli.disconnect()
    leaderboard.reset()
    OpenF1Interface.client = None


@app.get("/datas", response_model=list[DriverLive])
async def datas():
    cli = get_openf1_client()
    return leaderboard.read(cli.user_data_get()["drivers"])


@app.get("/results", response_model=list[DriverLive] | None)
async def results():
    cli = get_openf1_client()
    res = OpenF1Interface.get_results(
        cli.user_data_get()["access_token"],
        cli.user_data_get()["session_key"],
        cli.user_data_get()["drivers"]
    )
    if not res:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return res
