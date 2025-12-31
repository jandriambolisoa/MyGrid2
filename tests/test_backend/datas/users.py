import asyncio

from pydantic import BaseModel, ConfigDict
from starlette.testclient import TestClient

from backend.db.database import get_db
from backend.main import app
from backend.oauth2 import create_jwt_token
from backend.src.users.schemas import User, UserSelf
from backend.utils import random_code

class TestUser(BaseModel):
    user: UserSelf
    client: TestClient

    model_config = ConfigDict(arbitrary_types_allowed=True)

def predictable_password(username):
    return f"password123{username}*"

def create_random_user(client: TestClient, authorized: bool = False, moderator: bool = False, banned: bool = False):
    """
    Returns a valid random user and its client.
    Args:
        client: The TestClient to use.
        authorized: Whether the user to create is authorized.
        moderator: Whether the user to create is moderator.
        banned: Whether the user to create is banned.

    Returns:
        :class TestUser: The user as a Pydantic model.
    """
    db = get_db()
    name = random_code(12)
    user_data = {
        "username": name,
        "email":    f"{name}@example.com",
        "password": predictable_password(name)
    }

    client.post("/auth/signup", json=user_data)

    # Modify the verified entry if the user is authorized
    if authorized:
        db.cursor.execute("""
            UPDATE users
            SET verified = true
            WHERE username = %s
            RETURNING *""", (user_data["username"],))
        new_user = db.cursor.fetchone()
        db.conn.commit()

    else:
        db.cursor.execute("""
            SELECT *
            FROM users
            WHERE username = %s""", (user_data["username"],))
        new_user = db.cursor.fetchone()

    # Register the user role if he's a moderator
    if moderator:
        db.cursor.execute("""
            INSERT INTO promotedhistory (user_id, moderator, admin, by)
            VALUES (%s, %s, %s, %s)""", (new_user["id"], True, False, new_user["id"]))
        db.conn.commit()

    # Register the user in the banned users list if he's banned
    if banned:
        db.cursor.execute("""
            INSERT INTO bannedhistory (user_id, banned, by, reason)
            VALUES (%s, %s, %s, %s)""",(new_user["id"], True, new_user["id"], "Some random reason."))
        db.conn.commit()

    new_user["password"] = user_data["password"]

    access_token = asyncio.run(create_jwt_token({
        "user_id": new_user["id"],
        "username": new_user["username"],
        "language": "en"
    }))

    new_client = TestClient(app)
    new_client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}"
    }

    return TestUser(user=new_user, client=new_client)
