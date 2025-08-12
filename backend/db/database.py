import time

import psycopg
from psycopg.rows import dict_row
from psycopg.cursor import Cursor

from .config import settings
from ..config import settings as global_settings

class Database:
    conn = None

    def __init__(self):
        # According to psycopg 3 documentation
        # Connection objects are thread-safe but no Cursor object.
        # "However, cursors are lightweight objects: different threads
        # can create each one its own cursor to use independently from other threads."
        self.cursor = None

def init_db(
        db_host: str,
        db_port: int,
        db_name: str,
        db_user: str,
        db_password: str
    ):

    while True:
        print("DATABASE: Connecting...")

        conninfo = f"host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}"

        try:
            Database.conn = psycopg.connect(conninfo=conninfo, row_factory=dict_row)
            print("DATABASE: Successfully connected")
            break

        except Exception as e:
            print("DATABASE: Failed\n%s"%e)
            time.sleep(2)

def get_db():
    if not Database.conn:
        init_db(
            db_host=settings.db_host,
            db_port=settings.db_port,
            db_name=settings.db_name if not global_settings.debug else settings.db_name+"tests",
            db_user=settings.db_user,
            db_password=settings.db_password
        )
    db = Database()
    db.cursor = Database.conn.cursor()
    return db
