class DomainException(Exception):
    """Base exception for domain violations."""


class BusinessRuleViolationException(DomainException):
    """Exception raised when a business rule is violated."""


class InvalidEntityStateException(DomainException):
    """Exception raised when an entity is in an invalid state."""
