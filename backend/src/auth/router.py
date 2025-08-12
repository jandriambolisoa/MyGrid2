from fastapi import APIRouter, status, Depends
from psycopg.errors import UniqueViolation

from backend.exceptions import UnexpectedError
from backend.utils import hash
from backend.src.auth.syntax import valid_username, valid_password
from backend.src.users.schemas import UserCreate, UserSelf
from backend.db.database import get_db, Database

router = APIRouter(
    prefix="/auth",
    tags= ["auth"]
)


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserSelf)
def signup_user(user: UserCreate, language: str = None, db: Database = Depends(get_db)):
    # Removed the server maintenance condition
    # Me must worship a user initiative to sing-up and therefore
    # try our best to make it happen in any condition
    try:
        # Check credentials
        valid_username(user.username, language=language)
        valid_password(user.password, language=language)

        user.password = hash(user.password)

        # TODO: include add image at creation
        db.cursor.execute("""
            INSERT INTO users (username, email, password, language)
            VALUES (%s, %s, %s, %s)
            RETURNING *""", (user.username, user.email, user.password, language))
        new_user = db.cursor.fetchone()
        db.conn.commit()

        # TODO: add user in leaderboards

        # TODO: include automatic email verification
        #_send_verification_mail(user.username, user.email)

        # TODO include referral system

        # TODO: include full profile return
        return new_user

    except UniqueViolation as err:
        db.cursor.execute("ROLLBACK")
        db.conn.commit()
        raise UnexpectedError(language=language)
