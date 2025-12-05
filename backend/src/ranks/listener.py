from backend.db.database import get_db
from backend.src.users.schemas import UserSelf

from backend.src.scores.signals import updated_championship_scores

async def update_championship_ranks(championship_id: int, user: UserSelf):
    db = get_db()
    db.cursor.execute("""
        REFRESH MATERIALIZED VIEW ranks_championships_mv;""")
    db.conn.commit()

async def update_events_ranks(championship_id: int, user: UserSelf):
    db = get_db()
    db.cursor.execute("""
        REFRESH MATERIALIZED VIEW ranks_events_mv;""")
    db.conn.commit()

async def update_sessions_ranks(championship_id: int, user: UserSelf):
    db = get_db()
    db.cursor.execute("""
        REFRESH MATERIALIZED VIEW ranks_sessions_mv;""")
    db.conn.commit()


def init_listener():
    updated_championship_scores.connect(update_championship_ranks)
    updated_championship_scores.connect(update_events_ranks)
    updated_championship_scores.connect(update_sessions_ranks)
