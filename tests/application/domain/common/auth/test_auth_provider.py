from pytest import fixture, raises
from mediark.application.domain.common import (
    User, AuthProvider, StandardAuthProvider,
    AuthenticationError, AuthorizationError)


def test_auth_provider_repository_methods():
    abstract_methods = AuthProvider.__abstractmethods__  # type: ignore

    assert 'setup' in abstract_methods
    assert 'user' in abstract_methods
    assert 'roles' in abstract_methods
    assert 'validate_roles' in abstract_methods


@fixture
def auth_provider() -> StandardAuthProvider:
    # Given a memory auth_provider has been created
    auth_provider = StandardAuthProvider()
    auth_provider.setup(User(name="eecheverry"))
    return auth_provider


@fixture
def loaded_auth_provider(auth_provider) -> StandardAuthProvider:
    auth_provider.load({
        ("easb123")
    })
    return auth_provider


def test_standard_auth_provider(auth_provider):
    assert issubclass(StandardAuthProvider, AuthProvider)
    assert isinstance(auth_provider, AuthProvider)


def test_standard_auth_provider_verify(auth_provider):
    # Given a user
    user = User(name="asb123")
    # When a user is given
    auth_provider.setup(user)
    # Then the user will be set
    assert auth_provider.user is not None


def test_standard_auth_get_user(auth_provider):
    # When the get_user method is called
    user = auth_provider.user
    # Then the current request user is returned
    assert user.name == "eecheverry"


def test_standard_auth_roles_authenticated(auth_provider):
    # When the get_roles method is called and there is
    # a valid authentication
    auth_provider.setup(User(
        name='john',
        roles=['admin']))
    roles = auth_provider.roles
    assert roles == ['admin']


def test_standard_auth_get_roles_no_authenticated(auth_provider):
    # When the get_roles method is called and there isn't
    # a valid authentication
    auth_provider.setup(None)
    with raises(AuthenticationError):
        roles = auth_provider.roles


def test_standard_auth_validate_roles_correct_roles(auth_provider):
    # Given a list of roles, a list of required roles and a
    # authenticated user
    auth_provider.setup(User(name='john',  roles=['monitor']))
    required_roles = ["monitor", "admin"]
    # When a list of roles is set
    # Then the roles are validated
    auth_provider.validate_roles(required_roles)
    assert 'monitor' in auth_provider.roles


def test_standard_auth_validate_roles_incorrect_roles(auth_provider):
    # Given a list of roles, a list of required roles and a
    # authenticated user
    auth_provider.setup(User(name='john',  roles=['monitor']))
    required_roles = ["admin"]
    # When a list of roles is set
    # Then an authorizationerror is raised
    with raises(AuthorizationError):
        auth_provider.validate_roles(required_roles)


def test_standard_auth_raises_if_user_not_set(auth_provider):
    # Given an auth provider without user
    auth_provider.setup(None)
    # When the user property is invoked
    # Then an AuthenticationError is raised
    with raises(AuthenticationError):
        user = auth_provider.user
