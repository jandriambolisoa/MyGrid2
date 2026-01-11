import random

from starlette import status

from backend.utils import random_code
from tests.test_backend.datas.drivers import create_driver
from tests.test_backend.datas.events import get_competitive_sessions_from_event_id
from tests.test_backend.datas.users import MockUser


def mock_get_session_registrations(user_obj: MockUser, session):
    res = user_obj.client.get(f"/events/sessions/registrations/{session.id}")
    return res.status_code

def test_get_session_registrations(test_upcoming_events, test_passed_events, test_registrations, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    upcoming_event = random.choice(test_upcoming_events)
    upcoming_session = get_competitive_sessions_from_event_id(upcoming_event.id)[0]
    assert mock_get_session_registrations(unauthorized_user, upcoming_session) == status.HTTP_401_UNAUTHORIZED
    assert mock_get_session_registrations(unverified_user, upcoming_session) == status.HTTP_200_OK
    assert mock_get_session_registrations(authorized_user, upcoming_session) == status.HTTP_200_OK
    assert mock_get_session_registrations(moderator_user, upcoming_session) == status.HTTP_200_OK
    assert mock_get_session_registrations(banned_user, upcoming_session) == status.HTTP_401_UNAUTHORIZED

    passed_event = random.choice(test_passed_events)
    passed_session = get_competitive_sessions_from_event_id(passed_event.id)[0]
    assert mock_get_session_registrations(unauthorized_user, passed_session) == status.HTTP_401_UNAUTHORIZED
    assert mock_get_session_registrations(unverified_user, passed_session) == status.HTTP_200_OK
    assert mock_get_session_registrations(authorized_user, passed_session) == status.HTTP_200_OK
    assert mock_get_session_registrations(moderator_user, passed_session) == status.HTTP_200_OK
    assert mock_get_session_registrations(banned_user, passed_session) == status.HTTP_401_UNAUTHORIZED


def mock_override_session_registrations(user_obj: MockUser, session, drivers, teams):
    # Generate a new random registration grid
    number_of_drivers = len(drivers)
    registrations = list()
    random.shuffle(drivers)

    for i in range(number_of_drivers):
        registrations.append({
            "driver_id": drivers[i].id,
            "team_id": random.choice(teams).id,
            "prediction": i+1
        })

    res = user_obj.client.post(f"/events/sessions/registrations/{session.id}", json=registrations)
    return res.status_code

def test_override_session_registrations(test_upcoming_events, test_passed_events, test_drivers, test_teams, test_registrations, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    upcoming_event = random.choice(test_upcoming_events)
    upcoming_session = get_competitive_sessions_from_event_id(upcoming_event.id)[0]
    assert mock_override_session_registrations(unauthorized_user, upcoming_session, test_drivers, test_teams) == status.HTTP_401_UNAUTHORIZED
    assert mock_override_session_registrations(unverified_user, upcoming_session, test_drivers, test_teams) == status.HTTP_403_FORBIDDEN
    assert mock_override_session_registrations(authorized_user, upcoming_session, test_drivers, test_teams) == status.HTTP_403_FORBIDDEN
    assert mock_override_session_registrations(moderator_user, upcoming_session, test_drivers, test_teams) == status.HTTP_201_CREATED
    assert mock_override_session_registrations(banned_user, upcoming_session, test_drivers, test_teams) == status.HTTP_401_UNAUTHORIZED

    passed_event = random.choice(test_passed_events)
    passed_session = get_competitive_sessions_from_event_id(passed_event.id)[0]
    assert mock_override_session_registrations(unauthorized_user, passed_session, test_drivers, test_teams) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_override_session_registrations(unverified_user, passed_session, test_drivers, test_teams) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_override_session_registrations(authorized_user, passed_session, test_drivers, test_teams) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_override_session_registrations(moderator_user, passed_session, test_drivers, test_teams) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_override_session_registrations(banned_user, passed_session, test_drivers, test_teams) == status.HTTP_412_PRECONDITION_FAILED


def mock_swap_a_driver_with_an_unregistered_driver(user_obj: MockUser, session, drivers):
    # Create a new driver
    firstname = random_code(9, False, True)
    lastname = random_code(6, False, True)
    codename = lastname[:3]
    new_driver = create_driver(firstname, lastname, codename)

    old_driver = random.choice(drivers)

    res = user_obj.client.put(f"/events/sessions/registrations/{session.id}/swap-drivers", json={
        "old_driver_id": old_driver.id,
        "new_driver_id": new_driver.id,
        "new_driver_prediction": 1
    })

    return res.status_code


def test_swap_a_driver_with_an_unregistered_driver(test_upcoming_events, test_passed_events, test_drivers, test_registrations, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    upcoming_event = random.choice(test_upcoming_events)
    upcoming_session = get_competitive_sessions_from_event_id(upcoming_event.id)[0]
    assert mock_swap_a_driver_with_an_unregistered_driver(unauthorized_user, upcoming_session, test_drivers) == status.HTTP_401_UNAUTHORIZED
    assert mock_swap_a_driver_with_an_unregistered_driver(unverified_user, upcoming_session, test_drivers) == status.HTTP_403_FORBIDDEN
    assert mock_swap_a_driver_with_an_unregistered_driver(authorized_user, upcoming_session, test_drivers) == status.HTTP_403_FORBIDDEN
    assert mock_swap_a_driver_with_an_unregistered_driver(moderator_user, upcoming_session, test_drivers) == status.HTTP_200_OK
    assert mock_swap_a_driver_with_an_unregistered_driver(banned_user, upcoming_session, test_drivers) == status.HTTP_401_UNAUTHORIZED

    passed_event = random.choice(test_passed_events)
    passed_session = get_competitive_sessions_from_event_id(passed_event.id)[0]
    assert mock_swap_a_driver_with_an_unregistered_driver(unauthorized_user, passed_session, test_drivers) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_swap_a_driver_with_an_unregistered_driver(unverified_user, passed_session, test_drivers) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_swap_a_driver_with_an_unregistered_driver(authorized_user, passed_session, test_drivers) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_swap_a_driver_with_an_unregistered_driver(moderator_user, passed_session, test_drivers) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_swap_a_driver_with_an_unregistered_driver(banned_user, passed_session, test_drivers) == status.HTTP_412_PRECONDITION_FAILED


def mock_swap_teams_between_two_drivers(user_obj: MockUser, session, drivers):
    to_swap = iter(random.sample(drivers, 2))

    res = user_obj.client.put(f"/events/sessions/registrations/{session.id}/swap-teams", json={
        "driver_id_1": next(to_swap).id,
        "driver_id_2": next(to_swap).id
    })

    return res.status_code


def test_swap_teams_between_two_drivers(test_upcoming_events, test_passed_events, test_drivers, test_registrations, unauthorized_user, unverified_user, authorized_user, moderator_user, banned_user):
    upcoming_event = random.choice(test_upcoming_events)
    upcoming_session = get_competitive_sessions_from_event_id(upcoming_event.id)[0]
    assert mock_swap_a_driver_with_an_unregistered_driver(unauthorized_user, upcoming_session, test_drivers) == status.HTTP_401_UNAUTHORIZED
    assert mock_swap_a_driver_with_an_unregistered_driver(unverified_user, upcoming_session, test_drivers) == status.HTTP_403_FORBIDDEN
    assert mock_swap_a_driver_with_an_unregistered_driver(authorized_user, upcoming_session, test_drivers) == status.HTTP_403_FORBIDDEN
    assert mock_swap_a_driver_with_an_unregistered_driver(moderator_user, upcoming_session, test_drivers) == status.HTTP_200_OK
    assert mock_swap_a_driver_with_an_unregistered_driver(banned_user, upcoming_session, test_drivers) == status.HTTP_401_UNAUTHORIZED

    passed_event = random.choice(test_passed_events)
    passed_session = get_competitive_sessions_from_event_id(passed_event.id)[0]
    assert mock_swap_a_driver_with_an_unregistered_driver(unauthorized_user, passed_session, test_drivers) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_swap_a_driver_with_an_unregistered_driver(unverified_user, passed_session, test_drivers) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_swap_a_driver_with_an_unregistered_driver(authorized_user, passed_session, test_drivers) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_swap_a_driver_with_an_unregistered_driver(moderator_user, passed_session, test_drivers) == status.HTTP_412_PRECONDITION_FAILED
    assert mock_swap_a_driver_with_an_unregistered_driver(banned_user, passed_session, test_drivers) == status.HTTP_412_PRECONDITION_FAILED
