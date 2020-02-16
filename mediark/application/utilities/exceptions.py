
# Base


class ApplicationError(Exception):
    """Application's base error class."""

# Providers


class ProviderError(ApplicationError):
    """Providers' base error class."""


class TenantError(ProviderError):
    """Tenancy base error class."""


class TenantLocationError(TenantError):
    """The tenant location type was not found."""


class TenantCreationError(TenantError):
    """The tenant couldn't be created."""


class AuthError(ProviderError):
    """Auth error"""


class AuthenticationError(AuthError):
    """Authentication error"""


class AuthorizationError(ProviderError):
    """Authorization error"""

# Repository


class RepositoryError(ApplicationError):
    """Repositories' base error class."""


class EntityNotFoundError(RepositoryError):
    """The entity was not found in the repository."""


class EntityValidationError(RepositoryError):
    """Entity consistency validation error"""


# Coordinators


class EntityCreationError(ApplicationError):
    """Entity couldn't be created."""
