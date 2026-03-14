"""Unit tests for SchedulesSlotVO."""

from dataclasses import FrozenInstanceError
from datetime import time

import pytest

from src.contexts.admin.domain.value_objects.schedules_slot_vo import SchedulesSlotVO


class TestSchedulesSlotVOCreation:
    """Tests for SchedulesSlotVO creation and field access."""

    def test_should_create_successfully_with_valid_data(self):
        """Should create SchedulesSlotVO with valid data."""
        slot = SchedulesSlotVO(
            start_time=time(8, 0),
            end_time=time(9, 0),
            slot_duration_minutes=60,
            is_available=True,
        )

        assert slot.start_time == time(8, 0)
        assert slot.end_time == time(9, 0)
        assert slot.slot_duration_minutes == 60
        assert slot.is_available is True

    def test_should_create_with_is_available_false(self):
        """Should create SchedulesSlotVO with is_available set to False."""
        slot = SchedulesSlotVO(
            start_time=time(8, 0),
            end_time=time(9, 0),
            slot_duration_minutes=60,
            is_available=False,
        )

        assert slot.is_available is False

    def test_should_be_frozen_dataclass(self):
        """Should be immutable (frozen dataclass)."""
        slot = SchedulesSlotVO(
            start_time=time(8, 0),
            end_time=time(9, 0),
            slot_duration_minutes=60,
            is_available=True,
        )

        with pytest.raises(FrozenInstanceError):
            slot.start_time = time(9, 0)

    def test_should_create_with_30_minute_slots(self):
        """Should create SchedulesSlotVO with 30-minute slot duration."""
        slot = SchedulesSlotVO(
            start_time=time(8, 0),
            end_time=time(10, 0),
            slot_duration_minutes=30,
            is_available=True,
        )

        assert slot.slot_duration_minutes == 30

    def test_should_create_with_15_minute_slots(self):
        """Should create SchedulesSlotVO with 15-minute slot duration."""
        slot = SchedulesSlotVO(
            start_time=time(8, 0),
            end_time=time(9, 0),
            slot_duration_minutes=15,
            is_available=True,
        )

        assert slot.slot_duration_minutes == 15

    def test_should_create_with_minute_precision(self):
        """Should create SchedulesSlotVO with minute-precision times."""
        slot = SchedulesSlotVO(
            start_time=time(8, 30),
            end_time=time(9, 30),
            slot_duration_minutes=60,
            is_available=True,
        )

        assert slot.start_time == time(8, 30)
        assert slot.end_time == time(9, 30)


class TestSchedulesSlotVOValidation:
    """Tests for SchedulesSlotVO.validate()."""

    def test_validate_passes_with_valid_data(self):
        """Should not raise when all fields are valid."""
        slot = SchedulesSlotVO(
            start_time=time(8, 0),
            end_time=time(9, 0),
            slot_duration_minutes=60,
            is_available=True,
        )

        slot.validate()  # must not raise

    def test_validate_raises_when_end_time_equals_start_time(self):
        """Should raise ValueError when end_time equals start_time."""
        with pytest.raises(
            ValueError, match="end_time must be greater than start_time"
        ):
            SchedulesSlotVO(
                start_time=time(8, 0),
                end_time=time(8, 0),
                slot_duration_minutes=60,
                is_available=True,
            )

    def test_validate_raises_when_end_time_before_start_time(self):
        """Should raise ValueError when end_time is before start_time."""
        with pytest.raises(
            ValueError, match="end_time must be greater than start_time"
        ):
            SchedulesSlotVO(
                start_time=time(10, 0),
                end_time=time(8, 0),
                slot_duration_minutes=60,
                is_available=True,
            )

    def test_validate_raises_when_range_not_divisible_by_duration(self):
        """Should raise ValueError when time range is not divisible by slot duration."""
        with pytest.raises(
            ValueError, match="Time range must be divisible by slot duration"
        ):
            SchedulesSlotVO(
                start_time=time(8, 0),
                end_time=time(9, 0),
                slot_duration_minutes=40,
                is_available=True,
            )

    def test_validate_passes_when_range_exactly_divisible(self):
        """Should not raise when time range is exactly divisible by slot duration."""
        slot = SchedulesSlotVO(
            start_time=time(8, 0),
            end_time=time(10, 0),
            slot_duration_minutes=30,
            is_available=True,
        )

        slot.validate()  # must not raise

    def test_validate_passes_with_multiple_slot_durations(self):
        """Should accept 60, 30, and 15 minute durations for a 2-hour range."""
        for duration in [15, 30, 60, 120]:
            slot = SchedulesSlotVO(
                start_time=time(8, 0),
                end_time=time(10, 0),
                slot_duration_minutes=duration,
                is_available=True,
            )
            slot.validate()  # must not raise

    def test_validate_raises_for_7_minute_duration_in_60_minute_range(self):
        """Should raise ValueError for a non-divisible slot duration."""
        with pytest.raises(
            ValueError, match="Time range must be divisible by slot duration"
        ):
            SchedulesSlotVO(
                start_time=time(8, 0),
                end_time=time(9, 0),
                slot_duration_minutes=7,
                is_available=True,
            )


class TestSchedulesSlotVOToDict:
    """Tests for SchedulesSlotVO.to_dict()."""

    def test_to_dict_returns_correct_structure(self):
        """Should return a dict with all expected keys."""
        slot = SchedulesSlotVO(
            start_time=time(8, 0),
            end_time=time(9, 0),
            slot_duration_minutes=60,
            is_available=True,
        )

        result = slot.to_dict()

        assert "start_time" in result
        assert "end_time" in result
        assert "slot_duration_minutes" in result
        assert "is_available" in result

    def test_to_dict_start_time_is_iso_string(self):
        """start_time in dict must be an ISO-format string."""
        slot = SchedulesSlotVO(
            start_time=time(8, 30),
            end_time=time(9, 30),
            slot_duration_minutes=60,
            is_available=True,
        )

        result = slot.to_dict()

        assert result["start_time"] == "08:30"

    def test_to_dict_end_time_is_iso_string(self):
        """end_time in dict must be an ISO-format string."""
        slot = SchedulesSlotVO(
            start_time=time(8, 0),
            end_time=time(17, 0),
            slot_duration_minutes=60,
            is_available=True,
        )

        result = slot.to_dict()

        assert result["end_time"] == "17:00"

    def test_to_dict_slot_duration_minutes_is_int(self):
        """slot_duration_minutes in dict must be an integer."""
        slot = SchedulesSlotVO(
            start_time=time(8, 0),
            end_time=time(9, 0),
            slot_duration_minutes=60,
            is_available=True,
        )

        result = slot.to_dict()

        assert isinstance(result["slot_duration_minutes"], int)
        assert result["slot_duration_minutes"] == 60

    def test_to_dict_is_available_is_bool(self):
        """is_available in dict must be a boolean."""
        slot = SchedulesSlotVO(
            start_time=time(8, 0),
            end_time=time(9, 0),
            slot_duration_minutes=60,
            is_available=False,
        )

        result = slot.to_dict()

        assert isinstance(result["is_available"], bool)
        assert result["is_available"] is False

    def test_to_dict_preserves_all_values(self):
        """to_dict should preserve all field values correctly."""
        slot = SchedulesSlotVO(
            start_time=time(14, 30),
            end_time=time(16, 0),
            slot_duration_minutes=30,
            is_available=True,
        )

        result = slot.to_dict()

        assert result["start_time"] == "14:30"
        assert result["end_time"] == "16:00"
        assert result["slot_duration_minutes"] == 30
        assert result["is_available"] is True
