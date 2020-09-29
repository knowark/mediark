from pytest import fixture
from mediark.application.domain.services import User


@fixture
def user() -> User:
    return User()


def test_user_creation(user: User) -> None:
    assert isinstance(user, User)


def test_user_default_attributes(user: User) -> None:
    assert user.id == ""
    assert user.name == ""
    assert user.email == ""
    assert user.attributes == {}


def test_user_attributes_from_dict() -> None:

    user_dict = {
        "id": "XYZ123",
        "name": "Julian David Martos",
        "email": "jdmartos@nubark.com",
        "attributes": {
            "employee_id": "2349",
            "partner_id": "7689"
        }
    }

    user = User(**user_dict)

    for key, value in user_dict.items():
        assert getattr(user, key) == value
