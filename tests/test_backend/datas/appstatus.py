from backend.db.database import get_db

def create_appstatus(maintenance: bool, notes: str = "Some notes"):
    db = get_db()
    db.cursor.execute("""
        SELECT * FROM appstatus
        ORDER BY created DESC""")
    last_appstatus = db.cursor.fetchone()

    if last_appstatus is None:
        version = "2.0.0"

    else:
        version = ".".join(last_appstatus["version"].split(".")[0:-1])+f".{int(last_appstatus['version'].split('.')[-1])+1}"

    db.cursor.execute("""
        INSERT INTO appstatus (version, maintenance, notes)
        VALUES (%s, %s, %s)""", (version, maintenance, notes))
    db.conn.commit()
