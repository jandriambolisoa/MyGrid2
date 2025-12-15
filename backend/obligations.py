from http.client import HTTPException

from psycopg.errors import ForeignKeyViolation
from starlette import status

from backend import texts
from backend.db.database import get_db
from backend.schemas import ObligationResponse
from backend.src.users.exceptions import NotAUserError


#
# Obligations are like dialog messages that pops up whenever
# the user tries to do an action while we are expecting him
# to do something else. Those obligations will shows up
# instead of the expected response and are the only status_code 428
# of the application. We use those obligations to force the
# user to do certain action before continuing.
#

async def create_obligation(code: str, user_id: int, language: str = "en"):
    db = get_db()
    try:
        db.cursor.execute("""\
            INSERT INTO userobligations (user_id, obligation)
            VALUES (%s, %s)""", (user_id, code))
        db.conn.commit()
    except ForeignKeyViolation:
        db.conn.rollback()
        raise NotAUserError(language= language)


def obligation_content(code: str, language: str = "en"):
    """
    Return the content of an obligation response with the translated message.
    """
    obligations = {
        "newname": ObligationResponse(
            message= texts.obligation_newname[language],
            redirection= "/users/self/change_username",
            fields= {
                "new_username": "str"
            }
        ),
        "newpwd": ObligationResponse(
            message= texts.obligation_newpwd[language],
            redirection= "/users/self/change_password",
            fields= {
                "old_password": "str",
                "new_password": "str"
            }
        ),
    }
    return obligations[code]


class Obligation(HTTPException):
    status_code = status.HTTP_428_PRECONDITION_REQUIRED
    def __init__(self, code: str, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = {
            obligation_content(code, language).model_dump(mode= "json")
        }
