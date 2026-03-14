"""Unit tests for DoctorSchedulesEntity."""

from datetime import UTC, datetime, time
from uuid import UUID, uuid4

import pytest

from src.contexts.admin.domain.entities.doctor_schedules_entity import (
    DoctorSchedulesEntity,
)
from src.contexts.admin.domain.value_objects.doctor_weekly_schedules_vo import (
    DoctorWeeklySchedulesVO,
)
from src.contexts.admin.domain.value_objects.schedules_slot_vo import SchedulesSlotVO
from src.contexts.admin.domain.value_objects.timezone_vo import TimezoneVO
from src.shared.domain.exceptions.exception import MissingFieldException

# ─────────────────────────── helpers ────────────────────────────────────────


def _slot(start: time, end: time, duration: int = 60) -> SchedulesSlotVO:
    """Return a valid SchedulesSlotVO."""
    return SchedulesSlotVO(
        start_time=start,
        end_time=end,
        slot_duration_minutes=duration,
        is_available=True,
    )


def _valid_schedules() -> DoctorWeeklySchedulesVO:
    """Return a minimal valid DoctorWeeklySchedulesVO."""
    return DoctorWeeklySchedulesVO(
        schedules={"monday": [_slot(time(8, 0), time(9, 0))]}
    )


def _valid_timezone(tz: str = "UTC") -> TimezoneVO:
    """Return a valid TimezoneVO."""
    return TimezoneVO(timezone=tz)


# ─────────────────────────── creation – happy path ──────────────────────────


class TestDoctorSchedulesEntityCreate:
    """Tests for DoctorSchedulesEntity.create() factory method."""

    def test_should_create_successfully_with_valid_data(self):
        """Should return a DoctorSchedulesEntity instance with valid arguments."""
        doctor_id = uuid4()
        schedules = _valid_schedules()
        timezone = _valid_timezone()

        entity = DoctorSchedulesEntity.create(
            doctor_id=doctor_id,
            schedules=schedules,
            timezone=timezone,
        )

        assert isinstance(entity, DoctorSchedulesEntity)

    def test_should_store_doctor_id_correctly(self):
        """Created entity must expose the same doctor_id that was provided."""
        doctor_id = uuid4()

        entity = DoctorSchedulesEntity.create(
            doctor_id=doctor_id,
            schedules=_valid_schedules(),
            timezone=_valid_timezone(),
        )

        assert entity.doctor_id == doctor_id

    def test_should_store_schedules_correctly(self):
        """Created entity must expose the same schedules VO that was provided."""
        schedules = _valid_schedules()

        entity = DoctorSchedulesEntity.create(
            doctor_id=uuid4(),
            schedules=schedules,
            timezone=_valid_timezone(),
        )

        assert entity.schedules == schedules

    def test_should_store_timezone_correctly(self):
        """Created entity must expose the same timezone VO that was provided."""
        timezone = _valid_timezone("America/Bogota")

        entity = DoctorSchedulesEntity.create(
            doctor_id=uuid4(),
            schedules=_valid_schedules(),
            timezone=timezone,
        )

        assert entity.timezone == timezone

    def test_should_generate_a_uuid_id(self):
        """Entity id must be a UUID."""
        entity = DoctorSchedulesEntity.create(
            doctor_id=uuid4(),
            schedules=_valid_schedules(),
            timezone=_valid_timezone(),
        )

        assert isinstance(entity.id, UUID)
        assert entity.id is not None

    def test_should_generate_unique_ids(self):
        """Two separate create() calls must produce different ids."""
        args = {
            "doctor_id": uuid4(),
            "schedules": _valid_schedules(),
            "timezone": _valid_timezone(),
        }

        entity1 = DoctorSchedulesEntity.create(**args)
        entity2 = DoctorSchedulesEntity.create(**args)

        assert entity1.id != entity2.id

    def test_should_set_utc_created_at(self):
        """created_at must be a UTC-aware datetime."""
        entity = DoctorSchedulesEntity.create(
            doctor_id=uuid4(),
            schedules=_valid_schedules(),
            timezone=_valid_timezone(),
        )

        assert entity.created_at.tzinfo == UTC

    def test_should_set_utc_updated_at(self):
        """updated_at must be a UTC-aware datetime."""
        entity = DoctorSchedulesEntity.create(
            doctor_id=uuid4(),
            schedules=_valid_schedules(),
            timezone=_valid_timezone(),
        )

        assert entity.updated_at.tzinfo == UTC

    def test_created_at_and_updated_at_are_equal_on_creation(self):
        """created_at and updated_at should be the same instant at creation time."""
        entity = DoctorSchedulesEntity.create(
            doctor_id=uuid4(),
            schedules=_valid_schedules(),
            timezone=_valid_timezone(),
        )

        assert entity.created_at == entity.updated_at

    def test_timestamps_are_datetime_instances(self):
        """created_at and updated_at must be datetime instances."""
        entity = DoctorSchedulesEntity.create(
            doctor_id=uuid4(),
            schedules=_valid_schedules(),
            timezone=_valid_timezone(),
        )

        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)


# ─────────────────────────── creation – validation ──────────────────────────


class TestDoctorSchedulesEntityCreateValidation:
    """Tests for argument validation inside DoctorSchedulesEntity.create()."""

    def test_raises_missing_field_exception_when_doctor_id_is_none(self):
        """Should raise MissingFieldException when doctor_id is None."""
        with pytest.raises(MissingFieldException) as exc_info:
            DoctorSchedulesEntity.create(
                doctor_id=None,
                schedules=_valid_schedules(),
                timezone=_valid_timezone(),
            )

        assert exc_info.value.field == "doctor_id"

    def test_raises_missing_field_exception_when_schedules_is_none(self):
        """Should raise MissingFieldException when schedules is None."""
        with pytest.raises(MissingFieldException) as exc_info:
            DoctorSchedulesEntity.create(
                doctor_id=uuid4(),
                schedules=None,
                timezone=_valid_timezone(),
            )

        assert exc_info.value.field == "schedules"

    def test_raises_missing_field_exception_when_timezone_is_none(self):
        """Should raise MissingFieldException when timezone is None."""
        with pytest.raises(MissingFieldException) as exc_info:
            DoctorSchedulesEntity.create(
                doctor_id=uuid4(),
                schedules=_valid_schedules(),
                timezone=None,
            )

        assert exc_info.value.field == "timezone"

    def test_raises_value_error_when_schedules_validation_fails(self):
        """Should propagate ValueError raised by DoctorWeeklySchedulesVO.validate()."""
        # Build a DoctorWeeklySchedulesVO that bypasses __post_init__ so we can
        # inject overlapping slots and let entity.create() call validate() on it.
        overlapping_slots = [
            _slot(time(8, 0), time(10, 0)),
            _slot(time(9, 0), time(11, 0)),
        ]
        bad_schedules = DoctorWeeklySchedulesVO.__new__(DoctorWeeklySchedulesVO)
        object.__setattr__(bad_schedules, "schedules", {"monday": overlapping_slots})

        with pytest.raises(ValueError):
            DoctorSchedulesEntity.create(
                doctor_id=uuid4(),
                schedules=bad_schedules,
                timezone=_valid_timezone(),
            )

    def test_raises_value_error_when_timezone_validation_fails(self):
        """Should propagate ValueError raised by TimezoneVO.validate()."""
        # Build a TimezoneVO bypassing __post_init__ so we can inject a bad value
        # and let entity.create() call validate() on it.
        bad_timezone = TimezoneVO.__new__(TimezoneVO)
        object.__setattr__(bad_timezone, "timezone", "")

        with pytest.raises(ValueError, match="Timezone cannot be empty"):
            DoctorSchedulesEntity.create(
                doctor_id=uuid4(),
                schedules=_valid_schedules(),
                timezone=bad_timezone,
            )

    def test_missing_field_exception_for_doctor_id_has_correct_field_name(self):
        """MissingFieldException.field must be 'doctor_id' when that argument is None."""
        with pytest.raises(MissingFieldException) as exc_info:
            DoctorSchedulesEntity.create(
                doctor_id=None,
                schedules=_valid_schedules(),
                timezone=_valid_timezone(),
            )

        assert "doctor_id" in str(exc_info.value)

    def test_create_accepts_multiple_days_and_timezones(self):
        """Should create entity correctly with several days and a non-UTC timezone."""
        schedules = DoctorWeeklySchedulesVO(
            schedules={
                "monday": [
                    _slot(time(8, 0), time(12, 0)),
                    _slot(time(14, 0), time(18, 0)),
                ],
                "wednesday": [_slot(time(9, 0), time(13, 0))],
                "friday": [_slot(time(8, 0), time(17, 0), 30)],
            }
        )
        timezone = _valid_timezone("America/New_York")

        entity = DoctorSchedulesEntity.create(
            doctor_id=uuid4(),
            schedules=schedules,
            timezone=timezone,
        )

        assert entity.schedules == schedules
        assert entity.timezone == timezone
