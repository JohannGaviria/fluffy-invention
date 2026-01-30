"""This module contains the LoginAttemptsCacheKeyVO value object definition."""

from dataclasses import dataclass

from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.shared.domain.value_objects.cache_key_vo import CacheKeyVO


@dataclass(frozen=True)
class LoginAttemptsCacheKeyVO(CacheKeyVO):
    """Cache key for login attempts."""

    @classmethod
    def from_email(cls, email: EmailVO) -> "LoginAttemptsCacheKeyVO":
        """Create cache key from email.

        Args:
            email (str): The email address.

        Returns:
            LoginAttemptsCacheKey: The cache key.
        """
        key = f"cache:auth:login_attempts:{email.value}"
        return cls(key=key)
