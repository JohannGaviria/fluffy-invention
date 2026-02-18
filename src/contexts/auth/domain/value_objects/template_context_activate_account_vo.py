"""This module contains the TemplateContextActivateAccountVO value object."""

from dataclasses import dataclass
from typing import Any

from src.shared.domain.value_objects.template_context_vo import TemplateContextVO


@dataclass(frozen=True)
class TemplateContextActivateAccountVO(TemplateContextVO):
    """Value object for the template context used in account activation emails."""

    first_name: str
    last_name: str
    temporary_password: str
    activation_code: str
    expiration_minutes: int

    def validate(self) -> None:
        """Validate the template context for account activation.

        Raises:
            ValueError: If any required field is missing or invalid.
        """
        if not self.first_name:
            raise ValueError("First name cannot be empty")

        if not self.last_name:
            raise ValueError("Last name cannot be empty")

        if not self.temporary_password:
            raise ValueError("Temporary password cannot be empty")

        if not self.activation_code:
            raise ValueError("Activation code cannot be empty")

        if self.expiration_minutes <= 0:
            raise ValueError("Expiration minutes must be positive")

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization.

        Returns:
            dict: Dictionary representation of the template context.
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "temporary_password": self.temporary_password,
            "activation_code": self.activation_code,
            "expiration_minutes": self.expiration_minutes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TemplateContextActivateAccountVO":
        """Create instance from dictionary.

        Args:
            data (dict[str, any]): Dictionary representation of the template context.

        Returns:
            TemplateContextActivateAccountVO: Instance of the template context value object.
        """
        return cls(
            first_name=data["first_name"],
            last_name=data["last_name"],
            temporary_password=data["temporary_password"],
            activation_code=data["activation_code"],
            expiration_minutes=data["expiration_minutes"],
        )
