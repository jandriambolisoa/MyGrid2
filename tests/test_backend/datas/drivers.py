from backend.db.database import get_db
from backend.src.drivers.schemas import Team, Driver

def create_team(name: str, color: str):
    db = get_db()
    db.cursor.execute("""
        INSERT INTO teams (name, color)
        VALUES (%s, %s)
        RETURNING *
        """, (name, color,))
    new_team = db.cursor.fetchone()

    return Team(**new_team)

def create_driver(firstname: str, lastname: str, codename: str):
    db = get_db()
    db.cursor.execute("""
        INSERT INTO drivers (firstname, lastname, codename)
        VALUES (%s, %s, %s)
        RETURNING *
        """, (firstname, lastname, codename))
    new_driver = db.cursor.fetchone()

    return Driver(**new_driver)