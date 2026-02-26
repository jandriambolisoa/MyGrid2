import random

from starlette import status

from backend.db.database import get_db
from backend.utils import random_code
from tests.test_backend.datas.events import get_competitive_sessions_from_event_id, create_session, create_event
from tests.test_backend.datas.users import MockUser

def mock_get_championships_ranks(user_obj: MockUser, championship):
    res = user_obj.client.get(f"/ranks/championships/{championship.id}")
    return res.status_code

def test_get_championships_ranks(test_scores, test_championship, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    assert mock_get_championships_ranks(unauthorized_user, test_championship) == status.HTTP_401_UNAUTHORIZED
    assert mock_get_championships_ranks(unverified_user, test_championship) == status.HTTP_200_OK
    assert mock_get_championships_ranks(authorized_user, test_championship) == status.HTTP_200_OK
    assert mock_get_championships_ranks(moderator_user, test_championship) == status.HTTP_200_OK
    assert mock_get_championships_ranks(banned_user, test_championship) == status.HTTP_401_UNAUTHORIZED

def mock_get_events_ranks(user_obj: MockUser, event):
    res = user_obj.client.get(f"/ranks/events/{event.id}")
    return res.status_code


def test_get_events_ranks(test_scores, test_upcoming_events, test_passed_events, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    upcoming_event = random.choice(test_upcoming_events)
    passed_event = random.choice(test_passed_events)
    assert mock_get_events_ranks(unauthorized_user, passed_event) == status.HTTP_401_UNAUTHORIZED
    assert mock_get_events_ranks(unverified_user, passed_event) == status.HTTP_200_OK
    assert mock_get_events_ranks(authorized_user, passed_event) == status.HTTP_200_OK
    assert mock_get_events_ranks(authorized_user, upcoming_event) == status.HTTP_404_NOT_FOUND
    assert mock_get_events_ranks(moderator_user, passed_event) == status.HTTP_200_OK
    assert mock_get_events_ranks(moderator_user, upcoming_event) == status.HTTP_404_NOT_FOUND
    assert mock_get_events_ranks(banned_user, passed_event) == status.HTTP_401_UNAUTHORIZED


def mock_get_records_sessions_ranks(user_obj: MockUser, championship):
    res = user_obj.client.get(f"/ranks/records/sessions/{championship.id}")
    return res.status_code

def test_get_records_sessions_ranks(test_championship, test_scores, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    assert mock_get_records_sessions_ranks(unauthorized_user, test_championship) == status.HTTP_401_UNAUTHORIZED
    assert mock_get_records_sessions_ranks(unverified_user, test_championship) == status.HTTP_200_OK
    assert mock_get_records_sessions_ranks(authorized_user, test_championship) == status.HTTP_200_OK
    assert mock_get_records_sessions_ranks(moderator_user, test_championship) == status.HTTP_200_OK
    assert mock_get_records_sessions_ranks(banned_user, test_championship) == status.HTTP_401_UNAUTHORIZED
