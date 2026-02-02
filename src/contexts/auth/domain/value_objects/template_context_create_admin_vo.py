"""This module contains the TemplateContextCreateAdminVO value object."""

from dataclasses import dataclass
from typing import Any

from src.shared.domain.value_objects.template_context_vo import TemplateContextVO


@dataclass(frozen=True)
class TemplateContextCreateAdminVO(TemplateContextVO):
    """Value object for the template context used to create the first admin."""

    first_name: str
    last_name: str
    email: str
    temporary_password: str

    def validate(self) -> None:
        """Validate the template context for account activation.

        Raises:
            ValueError: If any required field is missing or invalid.
        """
        if not self.first_name and not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        if not self.last_name and not self.last_name.strip():
            raise ValueError("Last name cannot be empty")
        if not self.email and not self.email.strip():
            raise ValueError("Email cannot be empty")
        if not self.temporary_password and not self.temporary_password.strip():
            raise ValueError("Temporary password cannot be empty")

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization.

        Returns:
            dict: Dictionary representation of the template context.
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "temporary_password": self.temporary_password,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TemplateContextCreateAdminVO":
        """Create instance from dictionary.

        Args:
            data (dict[str, any]): Dictionary representation of the template context.

        Returns:
            TemplateContextCreateAdminVO: Instance of the template context value object.
        """
        return cls(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            temporary_password=data["temporary_password"],
        )
