from pytest import fixture, raises
from mediark.application.services import (
    AuthService, StandardAuthService, User)
from mediark.application.services import (AuthenticationError,
                                            AuthorizationError)


def test_auth_service_repository_methods():
    abstract_methods = AuthService.__abstractmethods__

    assert 'setup' in abstract_methods
    assert 'is_authenticated' in abstract_methods
    assert 'validate_roles' in abstract_methods
    assert 'user' in abstract_methods


@fixture
def auth_service() -> StandardAuthService:
    # Given a memory auth_service has been created
    auth_service = StandardAuthService(User(name="eecheverry"))
    return auth_service


@fixture
def loaded_auth_service(auth_service) -> StandardAuthService:
    auth_service.load({
        ("easb123")
    })
    return auth_service


def test_standard_auth_service(auth_service):
    assert issubclass(StandardAuthService, AuthService)
    assert isinstance(auth_service, AuthService)


def test_standard_auth_service_verify(auth_service):
    # Given a user
    user = User(name="asb123")
    # When a user is given
    auth_service.setup(user)
    # Then the user will be set
    assert auth_service.user is not None


def test_standard_auth_get_user(auth_service):
    # When the get_user method is called
    user = auth_service.user
    # Then the current request user is returned
    assert user.name == "eecheverry"

def test_standard_auth_get_roles_no_authenticated(auth_service):
    # When the get_roles method is called and there isn't
    # a valid authentication
    auth_service.state.user = None
    with raises(AuthenticationError):
        roles = auth_service.roles

# TODO : FIX permissions system

def test_standard_auth_validate_roles_correct_roles(auth_service):
    # Given a list of roles, a list of required roles and a
    # authenticated user
    auth_service.state.user = User(name='john', roles='monitor')
    required_roles = ["MONITOR", "ADMIN"]
    # When a list of roles is set
    # Then the roles are validated
    # auth_service.validate_roles(required_roles)
    # assert 'MONITOR' in auth_service.roles


# def test_standard_auth_validate_roles_incorrect_roles(auth_service):
#     # Given a list of roles, a list of required roles and a
#     # authenticated user
#     auth_service.state.user = User(name='john', roles=['monitor'])
#     required_roles = ["ADMIN"]
#     # When a list of roles is setted
#     # Then an authorizationerror is raised
#     with raises(AuthorizationError):
#         auth_service.validate_roles(required_roles)
