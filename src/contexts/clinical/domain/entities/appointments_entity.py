"""This module contains the definition of the AppointmentEntity class, which represents a clinical appointment in the system."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.contexts.clinical.domain.enums.appointments_status_enum import (
    AppointmentStatusEnum,
)
from src.shared.domain.entities.entity import BaseEntity


@dataclass
class AppointmentEntity(BaseEntity):
    """Entity representing a clinical appointment.

    Attributes:
        patient_id (UUID): The unique identifier of the patient.
        doctor_id (UUID): The unique identifier of the doctor.
        scheduled_date (datetime): The scheduled date and time of the appointment.
        duration_minutes (int): The duration of the appointment in minutes.
        status (AppointmentStatusEnum): The current status of the appointment.
        reason (str): The reason for the appointment.
        specialty_id (UUID | None): The unique identifier of the medical specialty, if applicable.
    """

    patient_id: UUID
    doctor_id: UUID
    scheduled_date: datetime
    duration_minutes: int
    status: AppointmentStatusEnum
    reason: str
    specialty_id: UUID | None = None
