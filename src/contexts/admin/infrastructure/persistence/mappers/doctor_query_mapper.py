"""This module contains the DoctorQueryMapper class, which is responsible for mapping between DoctorModel and DoctorSummaryVO."""

from src.contexts.admin.domain.value_objects.doctor_summary_vo import DoctorSummaryVO
from src.contexts.auth.infrastructure.persistence.models.model import DoctorModel


class DoctorQueryMapper:
    """Mapper for converting between DoctorModel and DoctorSummaryVO."""

    @staticmethod
    def to_vo(model: DoctorModel) -> DoctorSummaryVO:
        """Converts a DoctorModel to a DoctorSummaryVO.

        Args:
            model (DoctorModel): The DoctorModel to convert.

        Returns:
            DoctorSummaryVO: The converted DoctorSummaryVO.
        """
        return DoctorSummaryVO(doctor_id=model.id, is_active=model.is_active)
