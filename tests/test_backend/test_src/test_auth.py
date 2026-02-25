import random
from unittest.mock import AsyncMock, patch, MagicMock

import pytest
from starlette import status
from starlette.responses import RedirectResponse

from backend.db.database import get_db
from backend.src.auth.schemas import LoginResponse, AppleTokenData, AppleIdTokenData
from backend.src.users.schemas import UserSelf
from tests.test_backend.datas.users import predictable_password, create_random_user


@pytest.mark.parametrize("username, email, password, status_code", [
    ("Valid_Username-001", "valid01@example.com", "passwordA1*", status.HTTP_201_CREATED),
    ("short", "short@example.com", "passwordA1*", status.HTTP_406_NOT_ACCEPTABLE),
    ("SomeUser/001", "someuser@example.com", "passwordA1*", status.HTTP_406_NOT_ACCEPTABLE),
    ("HereIsATooLongUsernameForNoReason", "toolong@example.com", "passwordA1*", status.HTTP_406_NOT_ACCEPTABLE),
    ("wrong_email", "notAnEmail.com", "passwordA1*", status.HTTP_406_NOT_ACCEPTABLE),
    ("BADPW-01", "password01@example.com", "lowerUPPER", status.HTTP_406_NOT_ACCEPTABLE),
    ("BADPW-02", "password02@example.com", "lower2000", status.HTTP_406_NOT_ACCEPTABLE),
    ("BADPW-03", "password03@example.com", "lower*$-?", status.HTTP_406_NOT_ACCEPTABLE),
    ("BADPW-04", "password04@example.com", "UPPER2024", status.HTTP_406_NOT_ACCEPTABLE),
    ("BADPW-05", "password05@example.com", "UPPER?-*€", status.HTTP_406_NOT_ACCEPTABLE),
    ("BADPW-06", "password06@example.com", "2024**$?", status.HTTP_406_NOT_ACCEPTABLE),
    ("BADPW-07", "password07@example.com", "$h0rT", status.HTTP_406_NOT_ACCEPTABLE),
    ("BADPW-08", "password08@example.com", "lowerlower", status.HTTP_406_NOT_ACCEPTABLE),
    ("BADPW-09", "password09@example.com", "UPPERUPPER", status.HTTP_406_NOT_ACCEPTABLE),
    ("BADPW-10", "password10@example.com", "20242000", status.HTTP_406_NOT_ACCEPTABLE),
    ("BADPW-11", "password11@example.com", "$$**/&#€-_", status.HTTP_406_NOT_ACCEPTABLE),
])
def test_signup_user(username: str, email: str, password: str, status_code, client):
    with patch("backend.src.users.signals.created.send", return_value= None):
        # Create the user
        res = client.post("/auth/signup", json={
            "username": username,
            "email": email,
            "password": password
        })
        assert res.status_code == status_code

        if res.status_code == status.HTTP_201_CREATED:
            current_user = UserSelf(**res.json())
            assert current_user.username == username
            assert current_user.email == email

            # Try to recreate the same user
            res = client.post("/auth/signup/", json={
                "username": username,
                "email": email,
                "password": password
            })
            assert res.status_code == status.HTTP_406_NOT_ACCEPTABLE

            db = get_db()
            db.cursor.execute("""\
                DELETE FROM users
                WHERE username = %s""", (username,))
            db.conn.commit()

def mocking_login_email(user_obj):
    password = predictable_password(user_obj.user.username)
    # Try login with email and username
    res = user_obj.client.post("/auth/login-email", data={
        "username": user_obj.user.username,
        "password": password
    })

    yield res.status_code

    res = user_obj.client.post("/auth/login-email", data={
        "username": user_obj.user.email,
        "password": password
    })

    yield res.status_code

def test_login_email(unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    assert tuple(mocking_login_email(unauthorized_user)) == (status.HTTP_200_OK, status.HTTP_200_OK)
    assert tuple(mocking_login_email(unverified_user)) == (status.HTTP_200_OK, status.HTTP_200_OK)
    assert tuple(mocking_login_email(authorized_user)) == (status.HTTP_200_OK, status.HTTP_200_OK)
    assert tuple(mocking_login_email(moderator_user)) == (status.HTTP_200_OK, status.HTTP_200_OK)
    assert tuple(mocking_login_email(banned_user)) == (status.HTTP_401_UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED)

def mocking_login_refresh_token(user_obj):
    password = predictable_password(user_obj.user.username)
    res = user_obj.client.post("/auth/login-email", data={
        "username": user_obj.user.username,
        "password": password
    })

    yield res.status_code

    if res.status_code == status.HTTP_200_OK:
        tokens = LoginResponse(**res.json())
        tokens = {
            "access_token": {
                "access_token": tokens.access_token.access_token,
                "token_type": "bearer"
            },
            "refresh_token": {
                "refresh_token": tokens.refresh_token.refresh_token,
                "token_type": "bearer"
            }
        }

        res = user_obj.client.post("/auth/login-refresh-token", json=tokens)
        yield res.status_code

    else:
        yield res.status_code

def test_login_refresh_token(unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    assert tuple(mocking_login_refresh_token(unauthorized_user)) == (status.HTTP_200_OK, status.HTTP_200_OK)
    assert tuple(mocking_login_refresh_token(unverified_user)) == (status.HTTP_200_OK, status.HTTP_200_OK)
    assert tuple(mocking_login_refresh_token(authorized_user)) == (status.HTTP_200_OK, status.HTTP_200_OK)
    assert tuple(mocking_login_refresh_token(moderator_user)) == (status.HTTP_200_OK, status.HTTP_200_OK)
    assert tuple(mocking_login_refresh_token(banned_user)) == (status.HTTP_401_UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED)


def test_logout(client, test_npc_users, test_appstatus):
    user_obj = create_random_user(client, verified= True, authorized= True)
    token = user_obj.client.headers["Authorization"].split(" ")[1]

    res = user_obj.client.post("/auth/logout")

    assert res.status_code == status.HTTP_204_NO_CONTENT

    db = get_db()
    db.cursor.execute("""\
        SELECT *
        FROM revokedtokens
        WHERE token = %s""", (token,))
    assert db.cursor.fetchone()


def test_confirm_email(client):
    mock_unverified_user = create_random_user(client, authorized=True, verified=False)

    mock_token = MagicMock()
    mock_token.user_id = mock_unverified_user.user.id
    mock_token.username = mock_unverified_user.user.username
    mock_token.email = mock_unverified_user.user.email
    mock_token.language = mock_unverified_user.user.language

    mock_payload = {"language": "en"}

    with patch("backend.src.auth.router.verify_access_token", return_value=mock_token), \
            patch("backend.src.auth.router.jwt.decode", return_value=mock_payload), \
            patch("backend.src.auth.signals.validate_mail.send", return_value=None):

        res = mock_unverified_user.client.get("/auth/confirm-email?token=mock.jwt.token", follow_redirects=False)
        assert res.status_code == status.HTTP_307_TEMPORARY_REDIRECT
