"""This module contains the use case for assigning schedules to a doctor."""

from src.contexts.admin.application.dto.command import AssignDoctorSchedulesCommand
from src.contexts.admin.domain.entities.doctor_schedules_entity import (
    DoctorSchedulesEntity,
)
from src.contexts.admin.domain.exceptions.exception import (
    DoctorNotFoundException,
    DoctorScheduleAlreadyExistsException,
    InactiveDoctorException,
)
from src.contexts.admin.domain.ports.repositories.doctor_schedules_repository_port import (
    DoctorSchedulesRepositoryPort,
)
from src.contexts.admin.domain.value_objects.timezone_vo import TimezoneVO
from src.contexts.auth.domain.ports.repositories.doctor_repository_port import (
    DoctorRepositoryPort,
)


class AssignDoctorSchedulesUseCase:
    """Use case for assigning schedules to a doctor."""

    def __init__(
        self,
        doctor_repository_port: DoctorRepositoryPort,
        doctor_schedules_repository_port: DoctorSchedulesRepositoryPort,
    ):
        """Initialize the AssignDoctorSchedules use case with the required ports.

        Args:
            doctor_repository_port (DoctorRepositoryPort): Port for accessing doctor data.
            doctor_schedules_repository_port (DoctorSchedulesRepositoryPort):
                Port for accessing doctor schedules data.
        """
        self.doctor_repository_port = doctor_repository_port
        self.doctor_schedules_repository_port = doctor_schedules_repository_port

    async def execute(self, command: AssignDoctorSchedulesCommand) -> None:
        """Execute the use case to assign doctor schedules.

        Args:
            command (AssignDoctorSchedulesCommand): Command to assign doctor schedules.

        Raises:
            DoctorNotFoundException: If the doctor does not exist.
            InactiveDoctorException: If the doctor is inactive.
            DoctorScheduleAlreadyExistsException: If the doctor already has schedules assigned.
        """
        # Check if the doctor exists
        doctor = self.doctor_repository_port.find_by_id(command.doctor_id)
        if not doctor:
            raise DoctorNotFoundException()

        # Check if the doctor is active
        if not doctor.is_active:
            raise InactiveDoctorException()

        # Check if the doctor already has schedules assigned
        exists_schedule = (
            await self.doctor_schedules_repository_port.doctor_schedule_exists(
                command.doctor_id
            )
        )
        if exists_schedule:
            raise DoctorScheduleAlreadyExistsException()

        # Create the doctor schedules entity and save it to the repository
        entity = DoctorSchedulesEntity.create(
            doctor_id=command.doctor_id,
            schedules=command.to_vo(),
            timezone=TimezoneVO(command.timezone),
        )
        await self.doctor_schedules_repository_port.save(entity)
