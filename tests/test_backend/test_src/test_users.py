import random

from starlette import status

from tests.test_backend.datas.users import MockUser


def mock_search_users(user_obj: MockUser, query: str):
    res = user_obj.client.get("/users/search", params={"q": query})
    return res.status_code


def test_search_users(test_npc_users, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    existing_user = random.choice(test_npc_users)

    assert mock_search_users(unauthorized_user, existing_user.user.username) == status.HTTP_401_UNAUTHORIZED
    assert mock_search_users(unverified_user, existing_user.user.username) == status.HTTP_200_OK
    assert mock_search_users(authorized_user, existing_user.user.username) == status.HTTP_200_OK
    assert mock_search_users(moderator_user, existing_user.user.username) == status.HTTP_200_OK
    assert mock_search_users(banned_user, existing_user.user.username) == status.HTTP_401_UNAUTHORIZED

    assert mock_search_users(unauthorized_user, existing_user.user.username[:-2]) == status.HTTP_401_UNAUTHORIZED
    assert mock_search_users(unverified_user, existing_user.user.username[:-2]) == status.HTTP_200_OK
    assert mock_search_users(authorized_user, existing_user.user.username[:-2]) == status.HTTP_200_OK
    assert mock_search_users(moderator_user, existing_user.user.username[:-2]) == status.HTTP_200_OK
    assert mock_search_users(banned_user, existing_user.user.username[:-2]) == status.HTTP_401_UNAUTHORIZED

    not_existing_user = "unknown_user"

    assert mock_search_users(unauthorized_user, not_existing_user) == status.HTTP_401_UNAUTHORIZED
    assert mock_search_users(unverified_user, not_existing_user) == status.HTTP_404_NOT_FOUND
    assert mock_search_users(authorized_user, not_existing_user) == status.HTTP_404_NOT_FOUND
    assert mock_search_users(moderator_user, not_existing_user) == status.HTTP_404_NOT_FOUND
    assert mock_search_users(banned_user, not_existing_user) == status.HTTP_401_UNAUTHORIZED