"""This module contains the AppointmentStatusEnum enumeration definition."""

from enum import Enum


class AppointmentStatusEnum(str, Enum):
    """Enumeration representing the possible statuses of a clinical appointment.

    Attributes:
        PENDING (str): The appointment is pending confirmation.
        CONFIRMED (str): The appointment has been confirmed.
        CHECKED_IN (str): The patient has checked in for the appointment.
        IN_PROGRESS (str): The appointment is currently in progress.
        COMPLETED (str): The appointment has been completed.
        CANCELLED (str): The appointment has been cancelled.
    """

    PENDING = ("pending",)
    CONFIRMED = ("confirmed",)
    CHECKED_IN = ("checked_in",)
    IN_PROGRESS = ("in_progress",)
    COMPLETED = ("completed",)
    CANCELLED = "cancelled"
