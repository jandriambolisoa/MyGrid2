import os

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")

class Settings (BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    debug: int = 0

    mail_host: str
    mail_cryptage: str
    mail_port: int
    mail_userlabel: str
    mail_alias: str
    mail_domain: str
    mail_login: str
    mail_password: str

settings = Settings()