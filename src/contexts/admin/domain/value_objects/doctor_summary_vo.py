"""This module contains the DoctorSummaryVO class, which represents a doctor summary."""

from dataclasses import dataclass
from uuid import UUID

from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class DoctorSummaryVO(BaseValueObject):
    """Value object representing a doctor summary.

    Attributes:
        doctor_id (UUID): The unique identifier of the doctor.
        is_active (bool): Indicates if the doctor is active.
    """

    doctor_id: UUID
    is_active: bool

    def validate(self) -> None:
        """Validates the DoctorSummaryVO.

        Raises:
            ValueError: If the doctor_id is None.
        """
        if self.doctor_id is None:
            raise ValueError("Doctor id is required")
