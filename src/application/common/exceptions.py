class ApplicationException(Exception):
    """Base exception for application-layer violations."""

    default_code: str = "APPLICATION_ERROR"

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or self.default_code


class ValidationException(ApplicationException):
    """Raised when application-level validation fails (including stateful rules)."""

    default_code = "VALIDATION_ERROR"
