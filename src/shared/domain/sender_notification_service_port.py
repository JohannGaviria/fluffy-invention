"""This module contains the SenderNotificationServicePort abstract class."""

from abc import ABC, abstractmethod


class SenderNotificationServicePort(ABC):
    """Abstract port for sending notifications."""

    @abstractmethod
    def send(self, recipient: str, subject: str, body: str) -> None:
        """Send a notification to the specified recipient.

        Args:
            recipient (str): The recipient of the notification.
            subject (str): The subject of the notification.
            body (str): The body content of the notification.
        """
        pass
