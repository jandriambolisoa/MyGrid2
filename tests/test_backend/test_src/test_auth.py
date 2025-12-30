import pytest
from starlette import status

from backend.src.users.schemas import UserSelf


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
def test_signup_user(username: str, email: str, password: str, status_code, unauthorized_user):
    # Create the user
    res = unauthorized_user.client.post("/auth/signup", json={
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
        res = unauthorized_user.client.post("/auth/signup/", json={
            "username": username,
            "email": email,
            "password": password
        })
        assert res.status_code == status.HTTP_406_NOT_ACCEPTABLE

