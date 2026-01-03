import random

import pytest
from starlette.testclient import TestClient

from backend.db.database import get_db
from backend.main import app
from backend.utils import random_code, random_color

from tests.test_backend.datas import users as users_utils
from tests.test_backend.datas import drivers as drivers_utils, appstatus as appstatus_utils, events as events_utils

@pytest.fixture(scope="session")
def client():
    yield TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def test_appstatus():
    appstatus_utils.create_appstatus(maintenance= False)

@pytest.fixture(scope="session")
def test_npc_users(client):
    created_users = list()

    for i in range(10):
        user = users_utils.create_random_user(client, authorized= True)
        created_users.append(user)

    return created_users

@pytest.fixture(scope="session")
def test_drivers(client):
    created_drivers = list()
    for i in range(20):
        firstname = random_code(random.choice(range(3, 24)) ,digits=False)
        lastname = random_code(random.choice(range(3, 24)) ,digits=False)
        new = drivers_utils.create_driver(firstname.title(), lastname.title(), lastname[:3].upper())
        created_drivers.append(new)

    return created_drivers

@pytest.fixture(scope="session")
def test_teams(client):
    created_teams = list()
    for i in range(10):
        name = random_code(random.choice(range(3, 24)) ,digits=False)
        new = drivers_utils.create_team(name.title(), random_color())
        created_teams.append(new)

    return created_teams

@pytest.fixture(scope="session")
def test_championship(client):
    return events_utils.create_championship("F0 2050")

@pytest.fixture(scope="session")
def test_upcoming_events(client, test_championship, test_teams, test_drivers):
    created_events = list()
    for i in range(4):
        name = random_code(random.choice(range(3, 24)) ,digits=False)
        new = events_utils.create_event(name.title(), test_championship.id)
        created_events.append(new)

        events_utils.create_session("Practice 1", new.id, False)
        events_utils.create_session("Practice 2", new.id, False)
        events_utils.create_session("Practice 3", new.id, False)
        events_utils.create_session("Qualifying", new.id, True)
        events_utils.create_session("Race", new.id, True)

    return created_events

@pytest.fixture(scope="session")
def test_passed_events(client, test_championship, test_teams, test_drivers):
    created_events = list()
    for i in range(4):
        name = random_code(random.choice(range(3, 24)) ,digits=False)
        new = events_utils.create_event(name.title(), test_championship.id)
        created_events.append(new)

        events_utils.create_session("Practice 1", new.id, False, False)
        events_utils.create_session("Practice 2", new.id, False, False)
        events_utils.create_session("Practice 3", new.id, False, False)
        events_utils.create_session("Qualifying", new.id, True, False)
        events_utils.create_session("Race", new.id, True, False)

    return created_events

@pytest.fixture(scope="session")
def test_registrations(test_teams, test_drivers, test_upcoming_events, test_passed_events):
    db = get_db()

    number_of_drivers = len(test_drivers)
    number_of_teams = len(test_teams)
    events = test_passed_events+test_upcoming_events

    for event in events:
        # Get sessions of this event
        db.cursor.execute("""\
            SELECT id
            FROM sessions
            WHERE event_id = %s""", (event.id,))
        results = db.cursor.fetchall()

        for session in results:
            predictions = iter(random.sample(range(1, number_of_drivers + 1), k=number_of_drivers))

            for driver in test_drivers:
                driver_id = driver.id
                team_id = random.choice(test_teams).id
                prediction = next(predictions)
                db.cursor.execute("""\
                    INSERT INTO sessionsregistrations (session_id, driver_id, team_id, prediction)
                    VALUES (%s, %s, %s, %s)""", (session["id"], driver_id, team_id, prediction))

            db.conn.commit()

@pytest.fixture(scope="session")
def test_results(test_teams, test_drivers, test_passed_events, test_registrations):
    db = get_db()

    for event in test_passed_events:
        # Get sessions of this event
        db.cursor.execute("""\
            SELECT id
            FROM sessions
            WHERE event_id = %s""", (event.id,))
        results = db.cursor.fetchall()

        for session in results:
            # Get this event registrations
            db.cursor.execute("""\
                SELECT driver_id
                FROM sessionsregistrations
                WHERE session_id = %s""", (session["id"],))
            registrations = db.cursor.fetchall()

            number_of_drivers = len(registrations)

            session_results = iter(random.sample(range(1, number_of_drivers + 1), k=number_of_drivers))
            points = [25, 18, 12, 10, 8, 6, 4, 3, 2, 1]

            for registration in registrations:
                driver_id = registration["driver_id"]
                driver_result = next(session_results)
                driver_points = points[driver_result] if driver_result < len(points) else 0
                db.cursor.execute("""\
                    INSERT INTO sessionsresults (session_id, driver_id, result, points)
                    VALUES (%s, %s, %s, %s)""", (session["id"], driver_id, driver_result, driver_points))

            db.conn.commit()

@pytest.fixture(scope="session")
def test_predictions(test_npc_users, test_registrations, test_passed_events, test_upcoming_events):
    db = get_db()

    events = test_passed_events + test_upcoming_events

    for user in test_npc_users[:-1]:
        user_id = user.user.id

        for event in events:
            # Get sessions of this event
            db.cursor.execute("""\
                SELECT id
                FROM sessions
                WHERE event_id = %s""", (event.id,))
            results = db.cursor.fetchall()

            for session in results:
                # Get this event registrations
                db.cursor.execute("""\
                    SELECT driver_id
                    FROM sessionsregistrations
                    WHERE session_id = %s""", (session["id"],))
                registrations = db.cursor.fetchall()

                number_of_drivers = len(registrations)

                session_predictions = iter(random.sample(range(1, number_of_drivers + 1), k=number_of_drivers))

                for registration in registrations:
                    db.cursor.execute("""\
                        INSERT INTO sessionsresults (session_id, user_id, driver_id, mygrid, potential)
                        VALUES (%s, %s, %s, %s, %s)""", (session["id"], user_id, registration["driver_id"], next(session_predictions), random.randint(0, 99)))

                db.conn.commit()

@pytest.fixture(scope="session")
def test_scores(test_npc_users, test_predictions, test_results, test_passed_events):
    db = get_db()

    for user in test_npc_users[:-1]:
        user_id = user.user.id

        for event in test_passed_events:
            # Get sessions of this event
            db.cursor.execute("""\
                SELECT id
                FROM sessions
                WHERE event_id = %s""", (event.id,))
            results = db.cursor.fetchall()

            for session in results:
                # Get this event registrations
                db.cursor.execute("""\
                    SELECT driver_id, potential
                    FROM sessionspredictions
                    WHERE session_id = %s""", (session["id"],))
                registrations = db.cursor.fetchall()

                for registration in registrations:
                    score = [0, round(registration["potential"]/2), registration["potential"]][random.randint(0, 2)]

                    db.cursor.execute("""\
                        INSERT INTO scores (user_id, session_id, driver_id, score)
                        VALUES (%s, %s, %s, %s)""", (user_id, session["id"], registration["driver_id"], score))

                db.conn.commit()

    # Refresh all materialized views of rankings
    db.cursor.execute("""
            REFRESH MATERIALIZED VIEW ranks_championships_mv;
            REFRESH MATERIALIZED VIEW ranks_events_mv;
            REFRESH MATERIALIZED VIEW ranks_sessions_mv;""")
    db.conn.commit()

@pytest.fixture(scope="session")
def unauthorized_user(client):
    return users_utils.create_random_user(client)

@pytest.fixture(scope="session")
def authorized_user(client):
    return users_utils.create_random_user(client, authorized= True)

@pytest.fixture(scope="session")
def moderator_user(client):
    return users_utils.create_random_user(client, authorized= True, moderator= True)

@pytest.fixture(scope="session")
def banned_user(client):
    return users_utils.create_random_user(client, authorized= True, banned= True)
