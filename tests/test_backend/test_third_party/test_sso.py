from unittest.mock import AsyncMock, patch

import pytest
from starlette import status


async def mock_login_google(user_obj):
    # Mocking the google verification to return a valid user data object
    mock_google_data = AsyncMock()
    mock_google_data.email = user_obj.user.email
    mock_google_data.email_verified = True
    mock_google_data.sub = 9999999999999
    mock_google_data.hd = None

    with patch("backend.src.auth.router.verify_google_token", return_value=mock_google_data):
        res = user_obj.client.post(
            "/auth/login-google",
            params={"credential": "mock_token"}
        )

    return res.status_code

@pytest.mark.asyncio
async def test_login_google(client, unauthorized_user, authorized_user, moderator_user, banned_user):
    assert await mock_login_google(unauthorized_user) == status.HTTP_202_ACCEPTED
    assert await mock_login_google(authorized_user) == status.HTTP_202_ACCEPTED
    assert await mock_login_google(moderator_user) == status.HTTP_202_ACCEPTED
    assert await mock_login_google(banned_user) == status.HTTP_401_UNAUTHORIZED


async def mock_login_apple(user_obj):
    mock_apple_data = AsyncMock()
    mock_apple_data.access_token = "fake_access_token"
    mock_apple_data.token_type = "bearer"
    mock_apple_data.expires_in = 99
    mock_apple_data.id_token = "fake_id_token"

    mock_apple_id_data = AsyncMock()
    mock_apple_id_data.email = user_obj.user.email
    mock_apple_id_data.sub = "MockAppleId"


    with patch("backend.src.auth.router.validate_apple_token", return_value=mock_apple_data), \
            patch("backend.src.auth.router.verify_apple_id_token", return_value=mock_apple_id_data):
        token = "test_token"

        res = user_obj.client.post("/auth/login-apple", params={
            "credential": "mock_credential",
            "nonce": "mock_nonce",
        })

        return res.status_code


@pytest.mark.asyncio
async def test_login_apple(client, unauthorized_user, authorized_user, moderator_user, banned_user):
    assert await mock_login_apple(unauthorized_user) == status.HTTP_202_ACCEPTED
    assert await mock_login_apple(authorized_user) == status.HTTP_202_ACCEPTED
    assert await mock_login_apple(moderator_user) == status.HTTP_202_ACCEPTED
    assert await mock_login_apple(banned_user) == status.HTTP_401_UNAUTHORIZED