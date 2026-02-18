"""This module contains the base class for value objects in the domain layer."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseValueObject(ABC):
    """Base class for value objects in the domain layer."""

    def __post_init__(self) -> None:
        """Post-initialization hook to perform validation after the object is created."""
        self.validate()

    @abstractmethod
    def validate(self) -> None:  # pragma: no cover
        """Override this method to implement validation logic for the value object."""
        pass
