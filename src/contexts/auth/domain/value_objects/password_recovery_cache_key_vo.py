"""This module contains the PasswordRecoveryCacheKeyVO value object."""

from dataclasses import dataclass

from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.shared.domain.value_objects.cache_key_vo import CacheKeyVO


@dataclass(frozen=True)
class PasswordRecoveryCacheKeyVO(CacheKeyVO):
    """Value object for the cache key used in password recovery."""

    @classmethod
    def from_email(cls, email: EmailVO) -> "PasswordRecoveryCacheKeyVO":
        """Create cache key from email.

        Args:
            email (EmailVO): Email value object.

        Returns:
            PasswordRecoveryCacheKeyVO: Cache key for password recovery.
        """
        key = f"cache:auth:recovery_code:{email.value}"
        return cls(key=key)
