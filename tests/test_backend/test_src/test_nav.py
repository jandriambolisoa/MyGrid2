from starlette import status

from tests.test_backend.datas.users import MockUser

def mock_home_get_main_event(user_obj: MockUser, championship):
    res = user_obj.client.get(f"/nav/home/main-event", params={"championship_id": championship.id})
    return res.status_code

def test_home_get_main_event(test_championship, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    assert mock_home_get_main_event(unauthorized_user, test_championship) == status.HTTP_401_UNAUTHORIZED
    assert mock_home_get_main_event(unverified_user, test_championship) == status.HTTP_200_OK
    assert mock_home_get_main_event(authorized_user, test_championship) == status.HTTP_200_OK
    assert mock_home_get_main_event(moderator_user, test_championship) == status.HTTP_200_OK
    assert mock_home_get_main_event(banned_user, test_championship) == status.HTTP_401_UNAUTHORIZED