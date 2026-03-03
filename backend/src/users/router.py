import base64

import requests
from argon2 import verify_password
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.sql.functions import user
from starlette import status
from starlette.responses import StreamingResponse, Response, JSONResponse

from backend.constants import QUERY_LIMIT
from backend.config import settings as app_settings
from backend.db.database import Database, get_db
from backend.oauth2 import get_current_user, get_current_token
from backend.obligations import delete_obligation
from backend.src.auth.exceptions import WrongCredentialsError
from backend.src.auth.listener import send_verification_email
from backend.src.auth.router import logout
from backend.src.auth.schemas import ChangePassword, AccessToken
from backend.src.auth.syntax import valid_username, valid_password
from backend.src.collectibles.constants import CHUNK_SIZE
from backend.src.collectibles.dependencies import get_user_collectibles
from backend.src.images.dependencies import generate_user_image_name
from backend.src.users.dependencies import valid_user_username, get_current_user_language
from backend.src.users.exceptions import NoUserFoundError, CannotUpdateUsernameError
from backend.src.users.schemas import User, UserSelf, UserProfile
from backend.src.users.texts import successful_password_update_message, email_verification_sent_message
from backend.utils import verify, hash_password

router = APIRouter(
    prefix="/users",
    tags= ["users"]
)


@router.get("/search", response_model=list[User])
async def search_users(current_user: UserSelf = Depends(get_current_user), db: Database = Depends(get_db),
                 q: str = "",
                 limit: int = QUERY_LIMIT,
                 page: int = 0):
    search = "%" + q + "%"
    offset = limit * page

    db.cursor.execute("""
        SELECT *
        FROM users
        WHERE username LIKE %s
        AND id NOT IN (
            SELECT DISTINCT ON (bannedhistory.user_id) bannedhistory.user_id AS id
            FROM bannedhistory
            WHERE bannedhistory.banned = true            
            ORDER BY bannedhistory.user_id, bannedhistory.created DESC
            )
        EXCEPT
        SELECT *
        FROM users
        WHERE id = %s
        ORDER BY username ASC
        LIMIT %s OFFSET %s""", (search, current_user.id, limit, offset))
    results = db.cursor.fetchall()

    if not results:
        raise NoUserFoundError(current_user.language)

    # TODO : Implement full profile

    return results


@router.get("/profile", response_model=UserProfile)
async def get_user_profile(username: str = Depends(valid_user_username), current_user: UserSelf = Depends(get_current_user), db: Database = Depends(get_db)):
    """
    If no username is given, will return the current user profile.
    Args:
        username: optionnal, the user to look for
        current_user:
        db:

    Returns:
        UserProfile schema
    """
    if username:
        db.cursor.execute("""\
            SELECT * FROM users
            WHERE username = %s""", (username,))
        user = db.cursor.fetchone()

        user = User(**user)

    else:
        user = User(**current_user.model_dump())

    collectibles = await get_user_collectibles(user.id)

    return {
        "user": user,
        "collectibles": collectibles
    }

@router.put("/profile/edit/pp", status_code=status.HTTP_202_ACCEPTED)
async def update_user_profile_picture(image: UploadFile, db:Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    image_name = await generate_user_image_name(current_user.id)

    db.cursor.execute("""\
        SELECT image FROM users
        WHERE id = %s""", (current_user.id,))
    old_user = db.cursor.fetchone()

    db.cursor.execute("""\
        UPDATE users
        SET image = %s
        WHERE id = %s""", (image_name, current_user.id))
    db.conn.commit()

    files = {"file": (image.filename, image.file, image.content_type)}
    res = requests.post(f"{app_settings.ms_assets_url}/images/{image_name}", files=files)
    if old_user["image"] is not None:
        requests.delete(f"{app_settings.ms_assets_url}/images/{old_user['image']}.jpg")


@router.put("/profile/edit/username", status_code=status.HTTP_202_ACCEPTED)
async def update_user_profile_username(username: str, db:Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    # ONLY AVAILABLE IF AN OBLIGATION EXISTS FOR THIS
    db.cursor.execute("""\
        SELECT *
        FROM userobligations
        WHERE user_id = %s AND obligation = %s""", (current_user.id, "newname"))
    obligation = db.cursor.fetchone()

    if obligation is None:
        raise CannotUpdateUsernameError(current_user.language)

    username = valid_username(username, current_user.language)

    db.cursor.execute("""\
        UPDATE users
        SET username = %s
        WHERE id = %s""", (username, current_user.id))
    db.conn.commit()

    await delete_obligation("newname", current_user.id)


@router.put("/profile/edit/password", status_code=status.HTTP_202_ACCEPTED)
async def update_user_profile_password(datas: ChangePassword, db:Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user), current_token: AccessToken = Depends(get_current_token)):
    new_password = await valid_password(datas.new_password, current_user.language)

    db.cursor.execute("""\
        SELECT password FROM users
        WHERE id = %s""", (current_user.id,))
    user = db.cursor.fetchone()

    if not verify(datas.old_password, user["password"]):
        raise WrongCredentialsError(current_user.language)

    db.cursor.execute("""\
        UPDATE users
        SET password = %s
        WHERE id = %s""", (hash_password(new_password), current_user.id))
    db.conn.commit()

    await delete_obligation("newpwd", current_user.id)

    await logout(db, current_user, current_token)

    return {
        "message": successful_password_update_message[current_user.language]
    }

@router.get("/send-verification-email", status_code=status.HTTP_200_OK)
async def resend_verification_email(language: str = Depends(get_current_user_language), db:Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    await send_verification_email(current_user.id)

    return JSONResponse({
        "detail": email_verification_sent_message[language]
    })