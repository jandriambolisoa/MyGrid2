import random

from starlette import status

from backend.db.database import get_db
from backend.src.drivers.schemas import Driver, Team
from backend.utils import random_code, random_color
from tests.test_backend.datas.drivers import create_driver, create_team
from tests.test_backend.datas.users import MockUser


def mock_create_driver(user_obj: MockUser):
    firstname = random_code(9, digits=False, letters=True)
    lastname = random_code(9, digits=False, letters=True)
    driver_data = {
        "firstname": firstname.title(),
        "lastname": lastname.title(),
        "codename": lastname.upper()[:3]
    }
    res = user_obj.client.post("/drivers", json=driver_data)
    yield res.status_code

    if res.status_code == status.HTTP_201_CREATED:
        driver = Driver(**res.json())

        is_driver_firstname_correct = driver.firstname.lower() == driver_data["firstname"].lower()
        is_driver_lastname_correct = driver.lastname.lower() == driver_data["lastname"].lower()
        is_driver_codename_correct = driver.codename.lower() == driver_data["codename"].lower()

        yield all([is_driver_firstname_correct, is_driver_lastname_correct, is_driver_codename_correct])

    else:
        yield False


def test_create_driver(unauthorized_user, authorized_user, moderator_user, banned_user):
    assert tuple(mock_create_driver(unauthorized_user)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_create_driver(authorized_user)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_create_driver(moderator_user)) == (status.HTTP_201_CREATED, True)
    assert tuple(mock_create_driver(banned_user)) == (status.HTTP_401_UNAUTHORIZED, False)



def mock_create_team(user_obj: MockUser):
    name = random_code(9, digits=False, letters=True)
    color = random_color()
    team_data = {
        "name": name.title(),
        "color": color
    }
    res = user_obj.client.post("/drivers/teams", json=team_data)
    yield res.status_code

    if res.status_code == status.HTTP_201_CREATED:
        team = Team(**res.json())

        is_team_name_correct = team.name.lower() == team_data["name"].lower()
        is_team_color_correct = team.color.lower() == team_data["color"].lower()

        yield all([is_team_name_correct, is_team_color_correct])

    else:
        yield False


def test_create_team(unauthorized_user, authorized_user, moderator_user, banned_user):
    assert tuple(mock_create_team(unauthorized_user)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_create_team(authorized_user)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_create_team(moderator_user)) == (status.HTTP_201_CREATED, True)
    assert tuple(mock_create_team(banned_user)) == (status.HTTP_401_UNAUTHORIZED, False)


def mock_search_driver(user_obj: MockUser, q: str = None):
    res = user_obj.client.get("/drivers/search", params={"q": q})
    yield res.status_code


def test_search_driver(test_drivers, test_teams, test_registrations, unauthorized_user, authorized_user, moderator_user, banned_user):
    driver_to_search = random.choice(test_drivers)

    assert next(mock_search_driver(unauthorized_user)) == status.HTTP_200_OK
    assert next(mock_search_driver(authorized_user)) == status.HTTP_200_OK
    assert next(mock_search_driver(moderator_user)) == status.HTTP_200_OK
    assert next(mock_search_driver(banned_user)) == status.HTTP_200_OK

    assert next(mock_search_driver(unauthorized_user, "unknown driver")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_driver(authorized_user, "unknown driver")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_driver(moderator_user, "unknown driver")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_driver(banned_user, "unknown driver")) == status.HTTP_404_NOT_FOUND

    assert next(mock_search_driver(unauthorized_user, driver_to_search.firstname[1:-2])) == status.HTTP_200_OK
    assert next(mock_search_driver(authorized_user, driver_to_search.lastname[:-3])) == status.HTTP_200_OK
    assert next(mock_search_driver(moderator_user, driver_to_search.firstname)) == status.HTTP_200_OK
    assert next(mock_search_driver(banned_user, driver_to_search.codename)) == status.HTTP_200_OK


def mock_search_team(user_obj: MockUser, q: str = None):
    res = user_obj.client.get("/drivers/teams/search", params={"q": q})
    yield res.status_code


def test_search_team(test_drivers, test_teams, test_registrations, unauthorized_user, authorized_user, moderator_user, banned_user):
    team_to_search = random.choice(test_teams)

    assert next(mock_search_team(unauthorized_user)) == status.HTTP_200_OK
    assert next(mock_search_team(authorized_user)) == status.HTTP_200_OK
    assert next(mock_search_team(moderator_user)) == status.HTTP_200_OK
    assert next(mock_search_team(banned_user)) == status.HTTP_200_OK

    assert next(mock_search_team(unauthorized_user, "unknown team")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_team(authorized_user, "unknown team")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_team(moderator_user, "unknown team")) == status.HTTP_404_NOT_FOUND
    assert next(mock_search_team(banned_user, "unknown team")) == status.HTTP_404_NOT_FOUND

    assert next(mock_search_team(unauthorized_user, team_to_search.name[1:-2])) == status.HTTP_200_OK
    assert next(mock_search_team(authorized_user, team_to_search.name[:-3])) == status.HTTP_200_OK
    assert next(mock_search_team(moderator_user, team_to_search.name)) == status.HTTP_200_OK
    assert next(mock_search_team(banned_user, team_to_search.name[3:])) == status.HTTP_200_OK


def mock_update_driver(user_obj: MockUser):
    firstname = random_code(9, digits=False, letters=True).title()
    lastname = random_code(9, digits=False, letters=True).title()
    codename = lastname.upper()[:3]
    driver_to_update = create_driver(firstname, lastname, codename)

    new_firstname = random_code(9, digits=False, letters=True).title()
    new_lastname = random_code(9, digits=False, letters=True).title()
    new_codename = new_lastname.upper()[:3]

    res1 = user_obj.client.put(f"/drivers/{driver_to_update.id}", json={"firstname": new_firstname})
    res2 = user_obj.client.put(f"/drivers/{driver_to_update.id}", json={"lastname": new_lastname})
    res3 = user_obj.client.put(f"/drivers/{driver_to_update.id}", json={"codename": new_codename})

    updates_sucessful = all([
        res1.status_code == status.HTTP_200_OK,
        res2.status_code == status.HTTP_200_OK,
        res3.status_code == status.HTTP_200_OK
    ])

    yield res1.status_code
    yield res2.status_code
    yield res3.status_code

    if updates_sucessful:
        updated_driver = res3.json()
        is_driver_firstname_correct = updated_driver["firstname"].lower() == new_firstname.lower()
        is_driver_lastname_correct = updated_driver["lastname"].lower() == new_lastname.lower()
        is_driver_codename_correct = updated_driver["codename"].lower() == new_codename.lower()

        yield all([is_driver_firstname_correct, is_driver_lastname_correct, is_driver_codename_correct])

    else:
        yield False

def test_update_driver(test_drivers, unauthorized_user, authorized_user, moderator_user, banned_user):
    assert tuple(mock_update_driver(unauthorized_user)) == (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_update_driver(authorized_user)) == (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_update_driver(moderator_user)) == (status.HTTP_200_OK, status.HTTP_200_OK, status.HTTP_200_OK, True)
    assert tuple(mock_update_driver(banned_user)) == (status.HTTP_401_UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED, False)


def mock_update_team(user_obj: MockUser):
    name = random_code(12, digits=False, letters=True).title()
    color = random_color()
    team_to_update = create_team(name, color)

    new_name = random_code(12, digits=False, letters=True).title()
    new_color = random_color()

    res1 = user_obj.client.put(f"/drivers/teams/{team_to_update.id}", json={"name": new_name})
    res2 = user_obj.client.put(f"/drivers/teams/{team_to_update.id}", json={"color": new_color})

    updates_sucessful = all([
        res1.status_code == status.HTTP_200_OK,
        res2.status_code == status.HTTP_200_OK
    ])

    yield res1.status_code
    yield res2.status_code

    if updates_sucessful:
        updated_team = res2.json()
        is_team_name_correct = updated_team["name"].lower() == new_name.lower()
        is_team_color_correct = updated_team["color"].lower() == new_color.lower()

        yield all([is_team_name_correct, is_team_color_correct])

    else:
        yield False

def test_update_team(test_drivers, unauthorized_user, authorized_user, moderator_user, banned_user):
    assert tuple(mock_update_team(unauthorized_user)) == (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_update_team(authorized_user)) == (status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_update_team(moderator_user)) == (status.HTTP_200_OK, status.HTTP_200_OK, True)
    assert tuple(mock_update_team(banned_user)) == (status.HTTP_401_UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED, False)


def mock_delete_driver(user_obj: MockUser):
    driver_to_delete = create_driver(
        random_code(9, digits=False, letters=True).title(),
        random_code(9, digits=False, letters=True).title(),
        "AAA"
    )
    res = user_obj.client.delete(f"/drivers/{driver_to_delete.id}")
    yield res.status_code

    db = get_db()
    db.cursor.execute("""\
        SELECT *
        FROM drivers
        WHERE id = %s""", (driver_to_delete.id,))
    yield db.cursor.fetchone() is None


def test_delete_driver(unauthorized_user, authorized_user, moderator_user, banned_user):
    assert tuple(mock_delete_driver(unauthorized_user)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_delete_driver(authorized_user)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_delete_driver(moderator_user)) == (status.HTTP_204_NO_CONTENT, True)
    assert tuple(mock_delete_driver(banned_user)) == (status.HTTP_401_UNAUTHORIZED, False)


def mock_delete_team(user_obj: MockUser):
    team_to_delete = create_team(
        random_code(20, digits=False, letters=True).title(),
        random_color()
    )
    res = user_obj.client.delete(f"/drivers/teams/{team_to_delete.id}")
    yield res.status_code

    db = get_db()
    db.cursor.execute("""\
        SELECT *
        FROM teams
        WHERE id = %s""", (team_to_delete.id,))
    yield db.cursor.fetchone() is None


def test_delete_team(unauthorized_user, authorized_user, moderator_user, banned_user):
    assert tuple(mock_delete_team(unauthorized_user)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_delete_team(authorized_user)) == (status.HTTP_403_FORBIDDEN, False)
    assert tuple(mock_delete_team(moderator_user)) == (status.HTTP_204_NO_CONTENT, True)
    assert tuple(mock_delete_team(banned_user)) == (status.HTTP_401_UNAUTHORIZED, False)
