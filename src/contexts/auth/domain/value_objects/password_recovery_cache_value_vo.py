"""This module contains the PasswordRecoveryCacheValueVO value object."""

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.shared.domain.value_objects.cache_value_vo import CacheValueVO


@dataclass(frozen=True)
class PasswordRecoveryCacheValueVO(CacheValueVO):
    """Value object for the cache value used in password recovery."""

    user_id: UUID
    email: EmailVO
    recovery_code: str

    def validate(self) -> None:
        """Validate the cache value for password recovery.

        Raises:
            ValueError: If any validation fails.
        """
        if not self.user_id:
            raise ValueError("user_id cannot be empty")

        if not self.email:
            raise ValueError("email cannot be empty")

        if not self.recovery_code or not self.recovery_code.strip():
            raise ValueError("Code cannot be empty")

        if len(self.recovery_code) > 6:
            raise ValueError("Recovery code too long")

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization.

        Returns:
            dict: Dictionary representation of the cache value.
        """
        return {
            "user_id": str(self.user_id),
            "email": self.email.value,
            "recovery_code": self.recovery_code,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PasswordRecoveryCacheValueVO":
        """Create instance from dictionary.

        Args:
            data (dict[str, any]): Dictionary representation of the cache value.

        Returns:
            PasswordRecoveryCacheValueVO: Instance of the cache value object.
        """
        return cls(
            user_id=UUID(data["user_id"]),
            email=EmailVO(data["email"]),
            recovery_code=data["recovery_code"],
        )
