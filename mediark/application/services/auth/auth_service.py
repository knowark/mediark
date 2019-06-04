from abc import ABC, abstractmethod
from typing import List, Dict, Any
from threading import local
from .errors import AuthenticationError, AuthorizationError
from .user import User


class AuthService(ABC):
    """Authentication and authorization service."""
    class Roles:
        ADMIN = "ADMIN"
        MONITOR = "MONITOR"
        SUPERVISOR = "SUPERVISOR"
        GUARD = "GUARD"

    @abstractmethod
    def setup(self, user: User) -> None:
        """Setup the AuthService for the current user"""

    @property
    @abstractmethod
    def roles(self) -> List[str]:
        """Get current user roles"""

    @property
    @abstractmethod
    def user(self) -> User:
        """Get the current request user"""

    @abstractmethod
    def validate_roles(self, required_roles: List[str]=None):
        """Check if a user is authenticated"""

    @abstractmethod
    def is_authenticated(self) -> bool:
        """Check if a user is authenticated"""


class StandardAuthService(AuthService):

    def __init__(self, user=None) -> None:
        self.state = local()
        self.state.__dict__.setdefault('user', user)

        # self.authenticated = False
        # self.roles = []  # type: List[str]
        # self.user = User(name="User")

    def setup(self, user: User) -> None:
        self.state.user = user

    @property
    def roles(self) -> List[str]:
        if not self.is_authenticated():
            raise AuthenticationError(
                "Authentication is required to get the user's roles.")
        return [role.upper() for role in self.state.user.roles]

    @property
    def user(self) -> User:
        return self.state.user

    def validate_roles(self, required_roles: List[str]=None) -> None:
        required_roles = required_roles or []
        required_roles.append(self.Roles.ADMIN)
        required_roles_set = set(required_roles)
        roles_set = set(self.roles)
        if not roles_set & required_roles_set:
            raise AuthorizationError("Unable to validate roles.")

    def is_authenticated(self) -> bool:
        return bool(self.state.user)
