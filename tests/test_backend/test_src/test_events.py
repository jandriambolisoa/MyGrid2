import json
import random
from datetime import datetime, UTC, timedelta

from starlette import status

from backend.db.database import get_db
from backend.openf1.schemas import Driver
from backend.src.drivers.schemas import Team
from backend.src.events.schemas import Championship, Event
from backend.utils import random_code, random_color
from tests.test_backend.datas.events import create_championship, create_event, create_session
from tests.test_backend.datas.users import MockUser


def mock_create_championship(user_obj: MockUser):
    to_create_name = random_code(32, digits=False, letters=True)
    res = user_obj.client.post(f"/events/championships", json={"name": to_create_name})
    yield res.status_code

    if res.status_code == status.HTTP_201_CREATED:
        res = user_obj.client.post(f"/events/championships", json={"name": to_create_name})
        yield res.status_code == status.HTTP_409_CONFLICT
    else:
        yield True


def test_create_championship(unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    assert tuple(mock_create_championship(unauthorized_user)) == (status.HTTP_401_UNAUTHORIZED, True)
    assert tuple(mock_create_championship(unverified_user)) == (status.HTTP_403_FORBIDDEN, True)
    assert tuple(mock_create_championship(authorized_user)) == (status.HTTP_403_FORBIDDEN, True)
    assert tuple(mock_create_championship(moderator_user)) == (status.HTTP_201_CREATED, True)
    assert tuple(mock_create_championship(banned_user)) == (status.HTTP_401_UNAUTHORIZED, True)


def mock_create_event(user_obj: MockUser, championship: Championship):
    to_create_names = ({
        "en": random_code(32, digits=False, letters=True),
        "fr": random_code(32, digits=False, letters=True)
    })
    to_create_color = random_color()
    res = user_obj.client.post(f"/events", json={
        "name": to_create_names,
        "championship_id": championship.id,
        "color": to_create_color
    })
    yield res.status_code

    if res.status_code == status.HTTP_201_CREATED:
        res = user_obj.client.post(f"/events", json={
            "name": to_create_names,
            "championship_id": championship.id,
            "color": to_create_color
        })
        yield res.status_code == status.HTTP_409_CONFLICT
    else:
        yield True


def test_create_event(test_championship, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    assert tuple(mock_create_event(unauthorized_user, test_championship)) == (status.HTTP_401_UNAUTHORIZED, True)
    assert tuple(mock_create_event(unverified_user, test_championship)) == (status.HTTP_403_FORBIDDEN, True)
    assert tuple(mock_create_event(authorized_user, test_championship)) == (status.HTTP_403_FORBIDDEN, True)
    assert tuple(mock_create_event(moderator_user, test_championship)) == (status.HTTP_201_CREATED, True)
    assert tuple(mock_create_event(banned_user, test_championship)) == (status.HTTP_401_UNAUTHORIZED, True)


def mock_create_session(user_obj: MockUser, event: Event):
    to_create_names = ({
        "en": random_code(32, digits=False, letters=True),
        "fr": random_code(32, digits=False, letters=True)
    })
    to_create_datetime = datetime.now(UTC) + timedelta(days=1)

    session_data = {
        "name": to_create_names,
        "datetime": to_create_datetime.isoformat(),
        "event_id": event.id,
        "competitive": True
    }

    res = user_obj.client.post(f"/events/sessions", json=session_data)
    yield res.status_code

    if res.status_code == status.HTTP_201_CREATED:
        res = user_obj.client.post(f"/events/sessions", json=session_data)
        yield res.status_code == status.HTTP_409_CONFLICT
    else:
        yield True


def test_create_session(test_championship, test_upcoming_events, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    event = random.choice(test_upcoming_events)
    assert tuple(mock_create_session(unauthorized_user, event)) == (status.HTTP_401_UNAUTHORIZED, True)
    assert tuple(mock_create_session(unverified_user, event)) == (status.HTTP_403_FORBIDDEN, True)
    assert tuple(mock_create_session(authorized_user, event)) == (status.HTTP_403_FORBIDDEN, True)
    assert tuple(mock_create_session(moderator_user, event)) == (status.HTTP_201_CREATED, True)
    assert tuple(mock_create_session(banned_user, event)) == (status.HTTP_401_UNAUTHORIZED, True)


def mock_search_event(user_obj: MockUser, q: str = None):
    res = user_obj.client.get("/events/search", params={"q": q})
    yield res.status_code


def test_search_upcoming_event(test_upcoming_events, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    to_search = random.choice(test_upcoming_events)

    assert next(mock_search_event(unauthorized_user)) == status.HTTP_200_OK
    assert next(mock_search_event(unverified_user)) == status.HTTP_200_OK
    assert next(mock_search_event(authorized_user)) == status.HTTP_200_OK
    assert next(mock_search_event(moderator_user)) == status.HTTP_200_OK
    assert next(mock_search_event(banned_user)) == status.HTTP_200_OK

    assert next(mock_search_event(unauthorized_user, "unknown event")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_event(unverified_user, "unknown event")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_event(authorized_user, "unknown event")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_event(moderator_user, "unknown event")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_event(banned_user, "unknown event")) == status.HTTP_404_NOT_FOUND

    assert next(mock_search_event(unauthorized_user, to_search.name[1:-2])) == status.HTTP_200_OK
    assert next(mock_search_event(unverified_user, to_search.name[1:-2])) == status.HTTP_200_OK
    assert next(mock_search_event(authorized_user, to_search.name[:-3])) == status.HTTP_200_OK
    assert next(mock_search_event(moderator_user, to_search.name)) == status.HTTP_200_OK
    assert next(mock_search_event(banned_user, to_search.name)) == status.HTTP_200_OK


def test_search_passed_event(test_passed_events, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    to_search = random.choice(test_passed_events)

    assert next(mock_search_event(unauthorized_user)) == status.HTTP_200_OK
    assert next(mock_search_event(unverified_user)) == status.HTTP_200_OK
    assert next(mock_search_event(authorized_user)) == status.HTTP_200_OK
    assert next(mock_search_event(moderator_user)) == status.HTTP_200_OK
    assert next(mock_search_event(banned_user)) == status.HTTP_200_OK

    assert next(mock_search_event(unauthorized_user, "unknown event")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_event(unverified_user, "unknown event")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_event(authorized_user, "unknown event")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_event(moderator_user, "unknown event")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_event(banned_user, "unknown event")) == status.HTTP_404_NOT_FOUND

    assert next(mock_search_event(unauthorized_user, to_search.name[1:-2])) == status.HTTP_200_OK
    assert next(mock_search_event(unverified_user, to_search.name[1:-2])) == status.HTTP_200_OK
    assert next(mock_search_event(authorized_user, to_search.name[:-3])) == status.HTTP_200_OK
    assert next(mock_search_event(moderator_user, to_search.name)) == status.HTTP_200_OK
    assert next(mock_search_event(banned_user, to_search.name)) == status.HTTP_200_OK


def mock_update_championship(user_obj: MockUser):
    to_update = create_championship(random_code(12, digits=False, letters=True))
    to_update_names = {
        "en": random_code(12, digits=False, letters=True),
        "fr": random_code(12, digits=False, letters=True)
    }
    res = user_obj.client.put(f"/events/championships/{to_update.id}", json={"name": json.dumps(to_update_names)})
    yield res.status_code

def test_update_championship(unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    assert next(mock_update_championship(unauthorized_user)) == status.HTTP_401_UNAUTHORIZED
    assert next(mock_update_championship(unverified_user)) == status.HTTP_403_FORBIDDEN
    assert next(mock_update_championship(authorized_user)) == status.HTTP_403_FORBIDDEN
    assert next(mock_update_championship(moderator_user)) == status.HTTP_200_OK
    assert next(mock_update_championship(banned_user)) == status.HTTP_401_UNAUTHORIZED


def mock_update_event(user_obj: MockUser, championship: Championship):
    to_update = create_event(random_code(12, digits=False, letters=True), championship.id)
    to_update_names = {
        "en": random_code(12, digits=False, letters=True),
        "fr": random_code(12, digits=False, letters=True)
    }
    to_update_color = random_color()

    res = user_obj.client.put(f"/events/{to_update.id}", json={"name": to_update_names})
    yield res.status_code

    res = user_obj.client.put(f"/events/{to_update.id}", json={"color": to_update_color})
    yield res.status_code


def test_update_event(test_championship, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    assert next(mock_update_event(unauthorized_user, test_championship)) == status.HTTP_401_UNAUTHORIZED
    assert next(mock_update_event(unverified_user, test_championship)) == status.HTTP_403_FORBIDDEN
    assert next(mock_update_event(authorized_user, test_championship)) == status.HTTP_403_FORBIDDEN
    assert next(mock_update_event(moderator_user, test_championship)) == status.HTTP_200_OK
    assert next(mock_update_event(banned_user, test_championship)) == status.HTTP_401_UNAUTHORIZED


def mock_update_session(user_obj: MockUser, event: Event):
    to_update = create_session(random_code(12, digits=False, letters=True), event.id, True)
    to_update_names = {
        "en": random_code(12, digits=False, letters=True),
        "fr": random_code(12, digits=False, letters=True)
    }
    to_update_datetime = datetime.now(UTC) + timedelta(days=1)

    res = user_obj.client.put(f"/events/sessions/{to_update.id}", json={"name": to_update_names})
    yield res.status_code

    res = user_obj.client.put(f"/events/sessions/{to_update.id}", json={"datetime": to_update_datetime.isoformat()})
    yield res.status_code


def test_update_session(test_championship, test_upcoming_events, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    event = random.choice(test_upcoming_events)
    assert next(mock_update_session(unauthorized_user, event)) == status.HTTP_401_UNAUTHORIZED
    assert next(mock_update_session(unverified_user, event)) == status.HTTP_403_FORBIDDEN
    assert next(mock_update_session(authorized_user, event)) == status.HTTP_403_FORBIDDEN
    assert next(mock_update_session(moderator_user, event)) == status.HTTP_200_OK
    assert next(mock_update_session(banned_user, event)) == status.HTTP_401_UNAUTHORIZED


def mock_delete_championship(user_obj: MockUser):
    to_delete = create_championship(random_code(12, digits=False, letters=True))
    res = user_obj.client.delete(f"/events/championships/{to_delete.id}")
    yield res.status_code

    db = get_db()
    db.cursor.execute("""\
        SELECT *
        FROM championships
        WHERE id = %s""", (to_delete.id,))
    yield db.cursor.fetchone() is None


def test_delete_driver(unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    assert tuple(mock_delete_championship(unauthorized_user)) == (status.HTTP_401_UNAUTHORIZED, False)
    assert tuple(mock_delete_championship(unverified_user)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_delete_championship(authorized_user)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_delete_championship(moderator_user)) == (status.HTTP_204_NO_CONTENT, True)
    assert tuple(mock_delete_championship(banned_user)) == (status.HTTP_401_UNAUTHORIZED, False)


def mock_delete_event(user_obj: MockUser, championship: Championship):
    to_delete = create_event(random_code(12, digits=False, letters=True), championship.id)
    res = user_obj.client.delete(f"/events/{to_delete.id}")
    yield res.status_code

    db = get_db()
    db.cursor.execute("""\
        SELECT *
        FROM events
        WHERE id = %s""", (to_delete.id,))
    yield db.cursor.fetchone() is None


def test_delete_event(test_championship, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    assert tuple(mock_delete_event(unauthorized_user, test_championship)) == (status.HTTP_401_UNAUTHORIZED, False)
    assert tuple(mock_delete_event(unverified_user, test_championship)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_delete_event(authorized_user, test_championship)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_delete_event(moderator_user, test_championship)) == (status.HTTP_204_NO_CONTENT, True)
    assert tuple(mock_delete_event(banned_user, test_championship)) == (status.HTTP_401_UNAUTHORIZED, False)


def mock_delete_session(user_obj: MockUser, event: Event):
    to_delete = create_session(random_code(12, digits=False, letters=True), event.id, True)
    res = user_obj.client.delete(f"/events/sessions/{to_delete.id}")
    yield res.status_code

    db = get_db()
    db.cursor.execute("""\
        SELECT *
        FROM sessions
        WHERE id = %s""", (to_delete.id,))
    yield db.cursor.fetchone() is None


def test_delete_sessions(test_championship, test_upcoming_events, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    event = random.choice(test_upcoming_events)
    assert tuple(mock_delete_session(unauthorized_user, event)) == (status.HTTP_401_UNAUTHORIZED, False)
    assert tuple(mock_delete_session(unverified_user, event)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_delete_session(authorized_user, event)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_delete_session(moderator_user, event)) == (status.HTTP_204_NO_CONTENT, True)
    assert tuple(mock_delete_session(banned_user, event)) == (status.HTTP_401_UNAUTHORIZED, False)


def mock_override_wdc_prediction(user_obj: MockUser, championship: Championship, driver: Driver):
    res = user_obj.client.post(f"/events/championships/{championship.id}/wdc-prediction", json={
        "driver_id": driver.id
    })
    return res.status_code

def test_override_wdc_prediction(test_championship, test_upcoming_events, test_drivers, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    driver = random.choice(test_drivers)
    assert mock_override_wdc_prediction(unauthorized_user, test_championship, driver) == status.HTTP_401_UNAUTHORIZED
    assert mock_override_wdc_prediction(unverified_user, test_championship, driver) == status.HTTP_200_OK
    assert mock_override_wdc_prediction(authorized_user, test_championship, driver) == status.HTTP_200_OK
    assert mock_override_wdc_prediction(moderator_user, test_championship, driver) == status.HTTP_200_OK
    assert mock_override_wdc_prediction(banned_user, test_championship, driver) == status.HTTP_401_UNAUTHORIZED


def mock_override_wcc_prediction(user_obj: MockUser, championship: Championship, team: Team):
    res = user_obj.client.post(f"/events/championships/{championship.id}/wcc-prediction", json={
        "team_id": team.id
    })
    return res.status_code

def test_override_wcc_prediction(test_championship, test_upcoming_events, test_drivers, test_teams, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    team = random.choice(test_teams)
    assert mock_override_wcc_prediction(unauthorized_user, test_championship, team) == status.HTTP_401_UNAUTHORIZED
    assert mock_override_wcc_prediction(unverified_user, test_championship, team) == status.HTTP_200_OK
    assert mock_override_wcc_prediction(authorized_user, test_championship, team) == status.HTTP_200_OK
    assert mock_override_wcc_prediction(moderator_user, test_championship, team) == status.HTTP_200_OK
    assert mock_override_wcc_prediction(banned_user, test_championship, team) == status.HTTP_401_UNAUTHORIZED
