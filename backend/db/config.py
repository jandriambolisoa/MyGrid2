import os

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")

class Settings (BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

settings = Settings()