"""This module contains the TemplateContextPasswordRecoveryVO value object."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.shared.domain.value_objects.template_context_vo import TemplateContextVO


@dataclass(frozen=True)
class TemplateContextPasswordRecoveryVO(TemplateContextVO):
    """Value object for the template context used in password recovery."""

    first_name: str
    last_name: str
    recovery_code: str
    expiration_minutes: int
    request_datetime: datetime
    request_ip: str
    request_user_agent: str

    def validate(self) -> None:
        """Validate the template context for password recovery.

        Raises:
            ValueError: If any required field is missing or invalid.
        """
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name cannot be empty")
        if not self.recovery_code or not self.recovery_code:
            raise ValueError("Recovery code cannot be empty")
        if self.expiration_minutes <= 0:
            raise ValueError("Expiration minutes must be positive")
        if not self.request_datetime:
            raise ValueError("Request datetime cannot be empty")
        if not self.request_ip or not self.request_ip.strip():
            raise ValueError("Request IP cannot be empty")
        if not self.request_user_agent or not self.request_user_agent.strip():
            raise ValueError("Request user agent cannot be empty")

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization.

        Returns:
            dict: Dictionary representation of the template context.
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "recovery_code": self.recovery_code,
            "expiration_minutes": self.expiration_minutes,
            "request_datetime": self.request_datetime,
            "request_ip": self.request_ip,
            "request_user_agent": self.request_user_agent,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TemplateContextPasswordRecoveryVO":
        """Create instance from dictionary.

        Args:
            data: Dictionary containing the data to create the instance.

        Returns:
            TemplateContextPasswordRecoveryVO: Instance created from the dictionary.
        """
        return cls(
            first_name=data["first_name"],
            last_name=data["last_name"],
            recovery_code=data["recovery_code"],
            expiration_minutes=data["expiration_minutes"],
            request_datetime=data["request_datetime"],
            request_ip=data["request_ip"],
            request_user_agent=data["request_user_agent"],
        )
