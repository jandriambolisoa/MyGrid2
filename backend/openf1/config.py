import os

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")

class Settings (BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    debug: int = 0

    openf1_api_url: str = "https://api.openf1.org/"
    openf1_api_username: str
    openf1_api_password: str
    openf1_token_url: str = "https://api.openf1.org/token"
    openf1_mqtt_broker: str = "mqtt.openf1.org"
    openf1_mqtt_port: int = 8883

settings = Settings()