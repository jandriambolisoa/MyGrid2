from backend.db.database import get_db


async def is_user_has_prono(user_id: int, session_id: int) -> bool:
    db = get_db()
    db.cursor.execute("""
        SELECT user_id
        FROM sessionspredictions
        WHERE user_id = %s
        AND session_id = %s""", (user_id, session_id))
    has_prono = db.cursor.fetchone()

    if has_prono:
        return True

    return False


async def get_user_wdc_prediction(user_id: int, championship_id: int) -> int | None:
    """
    Return the driver's id of the user's prediction for the WDC of id championship_id.
    Return None if there is no prediction.
    Args:
        user_id: The user id
        championship_id: The championship id

    Returns:
        int: The id of the driver of the user's prediction or None
    """
    db = get_db()
    db.cursor.execute("""\
        SELECT driver_id
        FROM wdcpredictions
        WHERE user_id = %s AND championship_id = %s""", (user_id, championship_id))
    prediction = db.cursor.fetchone()

    if not prediction:
        return None

    return prediction["driver_id"]


async def get_user_wcc_prediction(user_id: int, championship_id: int) -> int | None:
    """
    Return the team's id of the user's prediction for the WCC of id championship_id.
    Return None if there is no prediction.
    Args:
        user_id: The user id
        championship_id: The championship id

    Returns:
        int: The id of the team of the user's prediction or None
    """
    db = get_db()
    db.cursor.execute("""\
        SELECT team_id
        FROM wccpredictions
        WHERE user_id = %s AND championship_id = %s""", (user_id, championship_id))
    prediction = db.cursor.fetchone()

    if not prediction:
        return None

    return prediction["team_id"]
