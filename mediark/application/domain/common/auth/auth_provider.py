from abc import ABC, abstractmethod
from typing import List, Optional
from contextvars import ContextVar
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

    @property
    def reference(self) -> str:
        return self.user.id


user_var: ContextVar[Optional[User]] = ContextVar('user', default=None)


class StandardAuthProvider(AuthProvider):

    def setup(self, user: User) -> None:
        user_var.set(user)

    @property
    def user(self) -> User:
        user = user_var.get()
        if not user:
            raise AuthenticationError("Not authenticated.")
        return user

    @property
    def roles(self) -> List[str]:
        user = user_var.get()
        if not user:
            raise AuthenticationError(
                "Authentication is required to get the user's roles.")
        return user.roles

    def validate_roles(self, required_roles: List[str] = None) -> None:
        required_roles = required_roles or []
        required_roles.append(self.Roles.ADMIN)
        required_roles_set = set(required_roles)
        roles_set = set(self.roles)
        if not roles_set & required_roles_set:
            raise AuthorizationError("Unable to validate roles.")
