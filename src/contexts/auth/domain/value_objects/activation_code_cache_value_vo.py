"""This module contains the ActivationCodeCacheValueVO value object definition."""

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from src.contexts.auth.domain.value_objects.email_vo import EmailVO
from src.shared.domain.value_objects.cache_value_vo import CacheValueVO


@dataclass(frozen=True)
class ActivationCodeCacheValueVO(CacheValueVO):
    """Value object representing an activation code cache value."""

    user_id: UUID
    email: EmailVO
    code: str

    def validate(self) -> None:
        """Validate the activation code cache value.

        Raises:
            ValueError: If any field is invalid.
        """
        if not self.user_id:
            raise ValueError("user_id cannot be empty")

        if not self.email:
            raise ValueError("email cannot be empty")

        if not self.code and not self.code.strip():
            raise ValueError("Activation code cannot be empty")

        if len(self.code) > 6:
            raise ValueError("Activation code too long")

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization.

        Returns:
            dict: Dictionary representation of the cache value.
        """
        return {
            "user_id": str(self.user_id),
            "email": self.email.value,
            "code": self.code,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ActivationCodeCacheValueVO":
        """Create instance from dictionary.

        Args:
            data (dict[str, any]): Dictionary representation of the cache value.

        Returns:
            ActivationCodeCacheValueVO: Instance of the cache value object.
        """
        return cls(
            user_id=UUID(data["user_id"]),
            email=EmailVO(data["email"]),
            code=data["code"],
        )
