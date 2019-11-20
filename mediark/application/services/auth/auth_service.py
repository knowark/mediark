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
    def user(self) -> User:
        """Get the current request user"""

    @property
    @abstractmethod
    def roles(self) -> List[str]:
        """Get current user roles"""

    @abstractmethod
    def validate_roles(self, required_roles: List[str]=None):
        """Check if a user is authenticated"""

    @abstractmethod
    def is_authenticated(self) -> bool:
        """Check if a user is authenticated"""


class StandardAuthService(AuthService):

    def __init__(self, dominion, user=None) -> None:
        self.dominion = dominion
        self.state = local()
        self.state.__dict__.setdefault('user', user)

    def setup(self, user: User) -> None:
        self.state.user = user

    @property
    def user(self) -> User:
        return self.state.user

    @property
    def roles(self) -> List[str]:
        if not self.is_authenticated():
            raise AuthenticationError(
                "Authentication is required to get the user's roles.")
        dominion_dict = self.state.user.authorization.get(self.dominion, {})
        return [role.upper() for role in dominion_dict.get('roles', [])]

    def validate_roles(self, required_roles: List[str]=None) -> None:
        required_roles = required_roles or []
        required_roles.append(self.Roles.ADMIN)
        required_roles_set = set(required_roles)
        roles_set = set(self.roles)
        if not roles_set & required_roles_set:
            raise AuthorizationError("Unable to validate roles.")

    def is_authenticated(self) -> bool:
        return bool(self.state.user)
