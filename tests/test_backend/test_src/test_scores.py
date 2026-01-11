from starlette import status

from backend.utils import random_code
from tests.test_backend.datas.events import create_championship
from tests.test_backend.datas.users import MockUser


def mock_get_score_parameters_of_a_championship(user_obj: MockUser, championship):
    res = user_obj.client.get(f"/scores/parameters/{championship.id}")
    return res.status_code

def test_get_score_parameters_of_a_championship(test_championship, unauthorized_user, authorized_user, moderator_user, banned_user):
    assert mock_get_score_parameters_of_a_championship(unauthorized_user, test_championship) == status.HTTP_200_OK
    assert mock_get_score_parameters_of_a_championship(authorized_user, test_championship) == status.HTTP_200_OK
    assert mock_get_score_parameters_of_a_championship(moderator_user, test_championship) == status.HTTP_200_OK
    assert mock_get_score_parameters_of_a_championship(banned_user, test_championship) == status.HTTP_401_UNAUTHORIZED

def mock_override_score_parameters_of_a_championship(user_obj: MockUser):
    championship = create_championship(random_code(12))

    datas = {
        "position": [10, 6, 3],
        "top10": [8, 3, 1],
        "top5": [8, 3, 1],
        "top3": [10, 5, 2],
        "top1": [12, 6, 5],
        "penultimate": [6, 2, 1],
        "last": [10, 5, 2],
        "rarity1": [1, 0, 0],
        "rarity2": [3, 1, 0],
        "rarity3": [6, 2, 0],
        "rarity4": [9, 4, 0],
        "rarity5": [15, 6, 0],
        "rarity6": [25, 10, 0],
        "rarity7": [35, 10, 0],
        "rarity8": [40, 10, 0],
        "rarity9": [45, 10, 0],
        "rarity10": [48, 10, 0],
        "rarity11": [50, 10, 0],
        "rarity12": [52, 10, 0],
        "rarity13": [54, 10, 0],
        "rarity14": [56, 10, 0],
        "rarity15": [58, 10, 0],
        "rarity16": [60, 10, 0],
        "rarity17": [62, 10, 0],
        "rarity18": [64, 10, 0],
        "rarity19": [66, 10, 0],
        "rarity20": [68, 10, 0],
        "rarity21": [70, 10, 0],
    }

    res = user_obj.client.post(f"/scores/parameters/{championship.id}", json=datas)
    return res.status_code


def test_override_score_parameters_of_a_championship(test_championship, unauthorized_user, authorized_user, moderator_user, banned_user):
    assert mock_override_score_parameters_of_a_championship(unauthorized_user) == status.HTTP_403_FORBIDDEN
    assert mock_override_score_parameters_of_a_championship(authorized_user) == status.HTTP_403_FORBIDDEN
    assert mock_override_score_parameters_of_a_championship(moderator_user) == status.HTTP_201_CREATED
    assert mock_override_score_parameters_of_a_championship(banned_user) == status.HTTP_401_UNAUTHORIZED
