from backend.db.database import get_db, Database
from backend.src.users import exceptions as user_exceptions
from backend.utils import random_code

async def assign_user_referral(referral_code: str, user_id: int, language: str = "en"):
    db = get_db()
    db.cursor.execute("""
        SELECT id FROM users
        WHERE referralcode = %s""", (referral_code,))
    referral_user = db.cursor.fetchone()

    if referral_user:
        try:
            db.cursor.execute("""
                INSERT INTO referrals (user_id, referral)
                VALUES (%s, %s)""", (user_id, referral_user["id"]))
            db.conn.commit()
        except:
            db.conn.rollback()
            raise user_exceptions.NoUserFoundError(language=language)

async def create_unique_referral_code():
    """
    Create and return a unique referral code
    :return: str
    """
    db = get_db()
    db.cursor.execute("""
        SELECT referralcode FROM users""")
    all_referral_codes = db.cursor.fetchall()
    all_referral_codes = [index["referralcode"] for index in all_referral_codes]

    new_referral_code = random_code(9)
    while new_referral_code in all_referral_codes:
        new_referral_code = random_code(9)

    return new_referral_code