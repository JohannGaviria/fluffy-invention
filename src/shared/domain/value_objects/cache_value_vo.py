"""This module contains the base class for cache value objects."""

from abc import abstractmethod
from typing import Any, Self

from src.shared.domain.value_objects.value_object import BaseValueObject


class CacheValueVO(BaseValueObject):
    """Base class for cache values."""

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:  # pragma: no cover
        """Convert to dictionary for serialization.

        Returns:
            dict[str, Any]: Dictionary representation of the cache value.
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:  # pragma: no cover
        """Create instance from dictionary.

        Args:
            data (dict[str, Any]): Dictionary representation of the cache value.

        Returns:
            Self: Instance of the cache value object.
        """
        pass

    def validate(self) -> None:  # pragma: no cover
        """Base validation - override in subclasses."""
        pass
