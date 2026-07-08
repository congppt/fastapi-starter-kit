from typing import Protocol


class IHasher(Protocol):
    """Interface for hashing"""

    def hash(self, value: str) -> str:
        """Hash a value"""

    def verify(self, value: str, hash: str) -> bool:
        """Verify a value against a hash"""
