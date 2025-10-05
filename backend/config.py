import os

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")

class Settings (BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV)

    debug: int = 0

    # dbmate related settings
    database_url: str

    # Security related settings
    secret_key: str
    algorithm: str
    token_expires_minutes: int
    refresh_token_expires_minutes: int
    google_auth_expo_client_id: str
    google_auth_android_client_id: str
    google_auth_ios_client_id: str

    # Redirections related settings
    website_url: str
    confirmed_email_url: str

    # Microservices related settings
    ms_mailings_url: str

settings = Settings()