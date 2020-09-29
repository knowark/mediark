from pytest import fixture
from mediark.application.domain.common import User


@fixture
def user() -> User:
    return User()


def test_user_creation(user: User) -> None:
    assert isinstance(user, User)


def test_user_default_attributes(user: User) -> None:
    assert user.id == ""
    assert user.name == ""
    assert user.email == ""
    assert user.roles == []


def test_user_attributes_from_dict() -> None:

    user_dict = {
        "id": "46ab9e22-639c-400b-b17d-e1a579f2a7bf",
        "name": "Juan Camilo Vivanco",
        "email": "jcvivanco@nubark.com",
        "roles": ['user', 'admin']
    }

    user = User(**user_dict)

    for key, value in user_dict.items():
        assert getattr(user, key) == value
