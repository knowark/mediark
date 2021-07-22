from ....application.domain.common import ApplicationError


class InfrastructureError(ApplicationError):
    """Infrastructure's base error class."""


# Authentication

class AuthenticationError(InfrastructureError):
    """Authentication error class."""
