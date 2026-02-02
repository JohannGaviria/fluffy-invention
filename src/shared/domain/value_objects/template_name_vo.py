"""This module contains the TemplateNameVO value object."""

from dataclasses import dataclass

from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class TemplateNameVO(BaseValueObject):
    """Value object for template names."""

    name: str

    def validate(self) -> None:
        """Validates the TemplateNameVO instance.

        Raises:
            ValueError: If the name is empty or whitespace.
        """
        if not self.name:
            raise ValueError("Template name cannot be empty or whitespace")
