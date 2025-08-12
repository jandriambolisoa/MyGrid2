from backend.db.database import get_db

async def is_server_on_maintenance() -> bool:
    db = get_db()
    db.cursor.execute(""" \
        SELECT *
        FROM appstatus
        ORDER BY created DESC""")
    last_appstatus = db.cursor.fetchone()

    if last_appstatus["maintenance"]:
        return True

    return False