"""This module contains the exceptions related to the admin context."""

from src.shared.domain.exceptions.exception import BaseDomainException


class DoctorNotFoundException(BaseDomainException):
    """Exception raised for when the doctor cannot not found."""

    def __init__(self) -> None:
        """Initialize the DoctorNotFoundException."""
        super().__init__("The doctor not found.")


class InactiveDoctorException(BaseDomainException):
    """Exception raised for when the doctor is inactive."""

    def __init__(self) -> None:
        """Initialize the InactiveDoctorException."""
        super().__init__("The doctor is inactive in the system.")


class DoctorScheduleAlreadyExistsException(BaseException):
    """Exception raised for when the doctor already has an assigned schedule."""

    def __init__(self) -> None:
        """Initialize the DoctorScheduleAlreadyExistsException."""
        super().__init__("The doctor already has an assigned schedule.")
