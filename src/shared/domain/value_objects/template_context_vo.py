"""This module contains the TemplateContextVO value object."""

from abc import abstractmethod
from typing import Any, Self

from src.shared.domain.value_objects.value_object import BaseValueObject


class TemplateContextVO(BaseValueObject):
    """Value object for template rendering context."""

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert context to dictionary.

        Returns:
            dict[str, Any]: Dictionary representation of the context.
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Create context from dictionary.

        Args:
            data (dict[str, str]): Dictionary representation of the context.

        Returns:
            Self: Instance of the context value object.
        """
        pass

    def validate(self) -> None:
        """Base validation - override in subclasses."""
        pass
