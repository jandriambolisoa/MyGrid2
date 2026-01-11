import random

from starlette import status

from tests.test_backend.datas.events import get_competitive_sessions_from_event_id
from tests.test_backend.datas.users import MockUser


def mock_get_session_results(user_obj: MockUser, session):
    res = user_obj.client.get(f"/events/sessions/results/{session.id}")
    return res.status_code


def test_get_session_results(test_upcoming_events, test_passed_events, test_results, unauthorized_user, authorized_user, moderator_user, banned_user):
    upcoming_event = random.choice(test_upcoming_events)
    upcoming_session = get_competitive_sessions_from_event_id(upcoming_event.id)[0]
    assert mock_get_session_results(unauthorized_user, upcoming_session) == status.HTTP_404_NOT_FOUND
    assert mock_get_session_results(authorized_user, upcoming_session) == status.HTTP_404_NOT_FOUND
    assert mock_get_session_results(moderator_user, upcoming_session) == status.HTTP_404_NOT_FOUND
    assert mock_get_session_results(banned_user, upcoming_session) == status.HTTP_401_UNAUTHORIZED

    passed_event = random.choice(test_passed_events)
    passed_session = get_competitive_sessions_from_event_id(passed_event.id)[0]
    assert mock_get_session_results(unauthorized_user, passed_session) == status.HTTP_200_OK
    assert mock_get_session_results(authorized_user, passed_session) == status.HTTP_200_OK
    assert mock_get_session_results(moderator_user, passed_session) == status.HTTP_200_OK
    assert mock_get_session_results(banned_user, passed_session) == status.HTTP_401_UNAUTHORIZED


def mock_override_session_results(user_obj: MockUser, session, drivers):
    data = list()
    for i in range(len(drivers)):
        data.append({
            "driver_id": drivers[i].id,
            "result": i+1,
            "points": random.randint(0, 12)
        })

    res = user_obj.client.post(f"/events/sessions/results/{session.id}", json=data)
    return res.status_code


def test_override_session_results(test_upcoming_events, test_drivers, test_passed_events, test_results, unauthorized_user, authorized_user, moderator_user, banned_user):
    upcoming_event = random.choice(test_upcoming_events)
    upcoming_session = get_competitive_sessions_from_event_id(upcoming_event.id)[0]
    assert mock_override_session_results(unauthorized_user, upcoming_session, test_drivers) == status.HTTP_403_FORBIDDEN
    assert mock_override_session_results(authorized_user, upcoming_session, test_drivers) == status.HTTP_403_FORBIDDEN
    assert mock_override_session_results(moderator_user, upcoming_session, test_drivers) == status.HTTP_201_CREATED
    assert mock_override_session_results(banned_user, upcoming_session, test_drivers) == status.HTTP_401_UNAUTHORIZED

    passed_event = random.choice(test_passed_events)
    passed_session = get_competitive_sessions_from_event_id(passed_event.id)[0]
    assert mock_override_session_results(unauthorized_user, passed_session, test_drivers) == status.HTTP_403_FORBIDDEN
    assert mock_override_session_results(authorized_user, passed_session, test_drivers) == status.HTTP_403_FORBIDDEN
    assert mock_override_session_results(moderator_user, passed_session, test_drivers) == status.HTTP_201_CREATED
    assert mock_override_session_results(banned_user, passed_session, test_drivers) == status.HTTP_401_UNAUTHORIZED


def mock_remove_session_results(user_obj: MockUser, session):
    res = user_obj.client.delete(f"/events/sessions/results/{session.id}")
    return res.status_code


def test_remove_session_results(test_upcoming_events, test_drivers, test_passed_events, test_results, unauthorized_user, authorized_user, moderator_user, banned_user):
    upcoming_event = random.choice(test_upcoming_events)
    upcoming_session = get_competitive_sessions_from_event_id(upcoming_event.id)[0]
    assert mock_remove_session_results(unauthorized_user, upcoming_session) == status.HTTP_403_FORBIDDEN
    assert mock_remove_session_results(authorized_user, upcoming_session) == status.HTTP_403_FORBIDDEN
    assert mock_remove_session_results(moderator_user, upcoming_session) == status.HTTP_204_NO_CONTENT
    assert mock_remove_session_results(banned_user, upcoming_session) == status.HTTP_401_UNAUTHORIZED

    passed_event = random.choice(test_passed_events)
    passed_session = get_competitive_sessions_from_event_id(passed_event.id)[0]
    assert mock_remove_session_results(unauthorized_user, passed_session) == status.HTTP_403_FORBIDDEN
    assert mock_remove_session_results(authorized_user, passed_session) == status.HTTP_403_FORBIDDEN
    assert mock_remove_session_results(moderator_user, passed_session) == status.HTTP_204_NO_CONTENT
    assert mock_remove_session_results(banned_user, passed_session) == status.HTTP_401_UNAUTHORIZED

