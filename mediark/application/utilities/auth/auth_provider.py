from abc import ABC, abstractmethod
from typing import List
from threading import local
from ..exceptions import AuthenticationError, AuthorizationError
from .user import User


class AuthProvider(ABC):
    """Authentication and authorization service."""
    class Roles:
        ADMIN = "admin"
        USER = "user"

    @abstractmethod
    def setup(self, user: User) -> None:
        """Setup the AuthProvider for the current user"""

    @property
    @abstractmethod
    def user(self) -> User:
        """Get the current request user"""

    @property
    @abstractmethod
    def roles(self) -> List[str]:
        """Get current user roles"""

    @abstractmethod
    def validate_roles(self, required_roles: List[str] = None):
        """Check if a user is authenticated"""


class StandardAuthProvider(AuthProvider):

    def __init__(self, user=None) -> None:
        self.state = local()
        self.state.__dict__.setdefault('user', user)

    def setup(self, user: User) -> None:
        self.state.user = user

    @property
    def user(self) -> User:
        return self.state.user

    @property
    def roles(self) -> List[str]:
        if not self.state.user:
            raise AuthenticationError(
                "Authentication is required to get the user's roles.")
        return self.state.user.roles

    def validate_roles(self, required_roles: List[str] = None) -> None:
        required_roles = required_roles or []
        required_roles.append(self.Roles.ADMIN)
        required_roles_set = set(required_roles)
        roles_set = set(self.roles)
        if not roles_set & required_roles_set:
            raise AuthorizationError("Unable to validate roles.")
