from .base import ApplicationException


class ValidationException(ApplicationException):
    """Raised when application-level validation fails (including stateful rules)."""

    default_code = "VALIDATION_ERROR"
