class DomainException(Exception):
    """Base exception for domain violations."""

    default_code: str = "DOMAIN_ERROR"

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or self.default_code


class BusinessRuleViolationException(DomainException):
    """Exception raised when a business rule is violated."""

    default_code = "BUSINESS_RULE_VIOLATION"


class InvalidEntityStateException(DomainException):
    """Exception raised when an entity is in an invalid state."""

    default_code = "INVALID_ENTITY_STATE"
