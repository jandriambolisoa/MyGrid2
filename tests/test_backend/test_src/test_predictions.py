import random

from starlette import status

from backend.db.database import get_db
from backend.utils import random_code
from tests.test_backend.datas.events import get_competitive_sessions_from_event_id, create_session, create_event
from tests.test_backend.datas.users import MockUser


def test_get_user_prediction(
        test_npc_users,
        test_appstatus,
        test_passed_events,
        test_upcoming_events,
        test_predictions,
        test_results,
        test_scores):

    user_obj = random.choice(test_npc_users)
    passed_event = random.choice(test_passed_events)
    upcoming_event = random.choice(test_upcoming_events)

    passed_session = get_competitive_sessions_from_event_id(passed_event.id)[0]
    upcoming_session = get_competitive_sessions_from_event_id(upcoming_event.id)[0]

    res = user_obj.client.get(f"/events/sessions/predictions/{passed_session.id}")
    res_json = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert res_json.get("session_score", None) is not None
    predictions = res_json.get("predictions", None)
    if predictions:
        assert predictions[0].get("score", None) is not None

    res = user_obj.client.get(f"/events/sessions/predictions/{upcoming_session.id}")
    res_json = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert res_json.get("session_score", None) is None
    predictions = res_json.get("predictions", None)
    if predictions:
        assert predictions[0].get("score", None) is None


def mock_create_my_grid(user_obj: MockUser, event, drivers):
    # Get a test session
    session = get_competitive_sessions_from_event_id(event.id)[0]

    my_grid = [driver.id for driver in drivers]
    random.shuffle(my_grid)

    i = 1
    datas = list()
    for driver_id in my_grid:
        datas.append({"driver_id": driver_id, "mygrid": i})
        i += 1

    res = user_obj.client.post(f"/events/sessions/predictions/{session.id}", json={"predictions":datas})

    return res.status_code

def test_create_my_grid(test_passed_events, test_upcoming_events, test_drivers, test_scores_parameters, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    upcoming_event = random.choice(test_upcoming_events)
    passed_event = random.choice(test_passed_events)
    assert mock_create_my_grid(unauthorized_user, upcoming_event, test_drivers) == status.HTTP_401_UNAUTHORIZED
    assert mock_create_my_grid(unverified_user, upcoming_event, test_drivers) == status.HTTP_403_FORBIDDEN
    assert mock_create_my_grid(authorized_user, upcoming_event, test_drivers) == status.HTTP_201_CREATED
    assert mock_create_my_grid(authorized_user, passed_event, test_drivers) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_create_my_grid(moderator_user, upcoming_event, test_drivers) == status.HTTP_201_CREATED
    assert mock_create_my_grid(moderator_user, passed_event, test_drivers) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_create_my_grid(banned_user, upcoming_event, test_drivers) == status.HTTP_401_UNAUTHORIZED

def mock_delete_my_grid(user_obj: MockUser, event, drivers):
    mock_create_my_grid(user_obj, event, drivers)

    session = get_competitive_sessions_from_event_id(event.id)[0]
    res = user_obj.client.delete(f"/events/sessions/predictions/{session.id}")

    return res.status_code

def test_delete_my_grid(test_passed_events, test_upcoming_events, test_drivers, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    upcoming_event = random.choice(test_upcoming_events)
    passed_event = random.choice(test_passed_events)
    assert mock_delete_my_grid(unauthorized_user, upcoming_event, test_drivers) == status.HTTP_401_UNAUTHORIZED
    assert mock_delete_my_grid(unverified_user, upcoming_event, test_drivers) == status.HTTP_403_FORBIDDEN
    assert mock_delete_my_grid(authorized_user, upcoming_event, test_drivers) == status.HTTP_204_NO_CONTENT
    assert mock_delete_my_grid(authorized_user, passed_event, test_drivers) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_delete_my_grid(moderator_user, upcoming_event, test_drivers) == status.HTTP_204_NO_CONTENT
    assert mock_delete_my_grid(moderator_user, passed_event, test_drivers) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_delete_my_grid(banned_user, upcoming_event, test_drivers) == status.HTTP_401_UNAUTHORIZED