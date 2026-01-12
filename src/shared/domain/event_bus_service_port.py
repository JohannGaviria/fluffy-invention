"""This module contains the interface for the Event Bus Service Port."""

from abc import ABC, abstractmethod


class EventBusServicePort(ABC):
    """Abstract base class for Event Bus Service Port."""

    @abstractmethod
    def publisher(self, name: str, payload: dict) -> None:
        """Publish an event to the event bus.

        Args:
            name (str): The name of the event.
            payload (dict): The payload of the event.

        Returns:
            None
        """
        pass

    @abstractmethod
    def subscriber(self, name: str) -> dict:
        """Subscribe to an event from the event bus.

        Args:
            name (str): The name of the event.

        Returns:
            dict: The payload of the event.
        """
        pass
