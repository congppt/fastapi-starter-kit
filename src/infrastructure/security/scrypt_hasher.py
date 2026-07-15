from __future__ import annotations

import hashlib
import hmac
import os
from base64 import b64decode, b64encode


class ScryptHasher:
    """Password hasher using ``hashlib.scrypt`` (RFC 7914).

    Output format: ``{base64(salt)}${base64(derived_key)}``.
    """

    # CPU/memory cost: number of iterations (must be a power of 2).
    # Higher = slower hashing and more memory → harder for attackers to brute-force.
    # 2**14 (16384) is a common interactive-login baseline.
    _n = 2**14

    # Block size factor: controls internal memory block size (memory ≈ 128 * n * r bytes).
    # Higher r → more memory per hash. 8 is the usual default.
    _r = 8

    # Parallelization: how many independent lanes to compute.
    # Higher p uses more CPU cores; 1 is typical for password hashing.
    _p = 1

    # Random salt size (bytes). Unique per password so identical passwords
    # produce different hashes and rainbow tables don't help.
    _salt_size = 16

    def hash(self, value: str) -> str:
        """Create a salted scrypt hash for storage."""
        salt = os.urandom(self._salt_size)
        derived = hashlib.scrypt(
            value.encode("utf-8"),
            salt=salt,
            n=self._n,
            r=self._r,
            p=self._p,
        )
        # Persist salt + digest together so verify() can recreate the same inputs.
        return f"{b64encode(salt).decode('ascii')}${b64encode(derived).decode('ascii')}"

    def verify(self, value: str, hash: str) -> bool:
        """Return True if ``value`` matches the stored ``hash``."""
        try:
            salt_b64, digest_b64 = hash.split("$", 1)
            salt = b64decode(salt_b64.encode("ascii"))
            expected = b64decode(digest_b64.encode("ascii"))
        except (ValueError, TypeError):
            return False

        # Re-hash with the original salt and the same n/r/p/dklen.
        actual = hashlib.scrypt(
            value.encode("utf-8"),
            salt=salt,
            n=self._n,
            r=self._r,
            p=self._p,
        )
        # Constant-time compare avoids timing attacks on the digest bytes.
        return hmac.compare_digest(actual, expected)
