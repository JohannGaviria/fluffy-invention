"""This module contains the SendNotificationVO value object."""

from dataclasses import dataclass

from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class SendNotificationVO(BaseValueObject):
    """Value object for sending notifications."""

    recipient: str
    subject: str
    body: str

    def validate(self) -> None:
        """Validates the SendNotificationVO instance.

        Raises:
            ValueError: If any of the fields are empty.
        """
        if not self.recipient and not self.recipient.strip():
            raise ValueError("Recipient cannot be empty.")

        if not self.subject and not self.subject.strip():
            raise ValueError("Subject cannot be empty.")

        if not self.body and not self.body.strip():
            raise ValueError("Body cannot be empty.")
