"""This module contains the SenderNotificationServicePort abstract class."""

from abc import ABC, abstractmethod

from src.shared.domain.value_objects.send_notification_vo import SendNotificationVO


class SenderNotificationServicePort(ABC):
    """Abstract port for sending notifications."""

    @abstractmethod
    def send(self, notification: SendNotificationVO) -> None:
        """Send a notification to the specified recipient.

        Args:
            notification (SendNotificationVO): The notification to be sent.
        """
        pass
