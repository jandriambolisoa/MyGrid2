from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from backend.db.config import settings as db_settings

scheduler = BackgroundScheduler()

jobstores = {
    "default": SQLAlchemyJobStore(url=f"postgresql+psycopg://{db_settings.db_user}:{db_settings.db_password}@{db_settings.db_host}:{db_settings.db_port}/{db_settings.db_name}")
}

scheduler.configure(jobstores=jobstores)
