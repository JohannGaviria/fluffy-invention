"""Unit tests for DoctorWeeklySchedulesVO."""

from dataclasses import FrozenInstanceError
from datetime import time

import pytest

from src.contexts.admin.domain.value_objects.doctor_weekly_schedules_vo import (
    DoctorWeeklySchedulesVO,
)
from src.contexts.admin.domain.value_objects.schedules_slot_vo import SchedulesSlotVO

# ─────────────────────────── helpers ────────────────────────────────────────


def _slot(
    start: time, end: time, duration: int = 60, available: bool = True
) -> SchedulesSlotVO:
    """Return a valid SchedulesSlotVO."""
    return SchedulesSlotVO(
        start_time=start,
        end_time=end,
        slot_duration_minutes=duration,
        is_available=available,
    )


def _morning_slot() -> SchedulesSlotVO:
    return _slot(time(8, 0), time(12, 0), 60)


def _afternoon_slot() -> SchedulesSlotVO:
    return _slot(time(14, 0), time(18, 0), 60)


# ─────────────────────────── creation ───────────────────────────────────────


class TestDoctorWeeklySchedulesVOCreation:
    """Tests for DoctorWeeklySchedulesVO creation."""

    def test_should_create_successfully_with_one_day(self):
        """Should create with a single valid day."""
        vo = DoctorWeeklySchedulesVO(schedules={"monday": [_morning_slot()]})

        assert "monday" in vo.schedules

    def test_should_create_successfully_with_all_days(self):
        """Should create with all seven days."""
        all_days = {
            "monday": [_morning_slot()],
            "tuesday": [_morning_slot()],
            "wednesday": [_morning_slot()],
            "thursday": [_morning_slot()],
            "friday": [_morning_slot()],
            "saturday": [_morning_slot()],
            "sunday": [_morning_slot()],
        }

        vo = DoctorWeeklySchedulesVO(schedules=all_days)

        assert len(vo.schedules) == 7

    def test_should_create_with_multiple_slots_per_day(self):
        """Should create with multiple non-overlapping slots for a day."""
        vo = DoctorWeeklySchedulesVO(
            schedules={"monday": [_morning_slot(), _afternoon_slot()]}
        )

        assert len(vo.schedules["monday"]) == 2

    def test_should_create_with_empty_slots_list(self):
        """Should create when a day has an empty slot list."""
        vo = DoctorWeeklySchedulesVO(schedules={"monday": []})

        assert vo.schedules["monday"] == []

    def test_should_be_frozen_dataclass(self):
        """Should be immutable (frozen dataclass)."""
        vo = DoctorWeeklySchedulesVO(schedules={"monday": [_morning_slot()]})

        with pytest.raises(FrozenInstanceError):
            vo.schedules = {}


# ─────────────────────────── validate – days ────────────────────────────────


class TestDoctorWeeklySchedulesVOValidateDays:
    """Tests for day-level validation inside DoctorWeeklySchedulesVO.validate()."""

    def test_validate_passes_for_all_valid_days(self):
        """Should not raise for every valid day name."""
        for day in [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]:
            vo = DoctorWeeklySchedulesVO(schedules={day: [_morning_slot()]})
            vo.validate()  # must not raise

    def test_validate_raises_for_invalid_day_name(self):
        """Should raise ValueError for an unrecognised day name."""
        with pytest.raises(ValueError, match="Invalid day"):
            DoctorWeeklySchedulesVO(schedules={"funday": [_morning_slot()]})

    def test_validate_raises_when_schedules_is_none(self):
        """Should raise ValueError when schedules dict is None."""
        vo = DoctorWeeklySchedulesVO.__new__(DoctorWeeklySchedulesVO)
        object.__setattr__(vo, "schedules", None)

        with pytest.raises(ValueError, match="Schedules cannot be empty"):
            vo.validate()

    def test_validate_raises_when_slots_value_is_not_a_list(self):
        """Should raise ValueError when a day maps to a non-list value."""
        vo = DoctorWeeklySchedulesVO.__new__(DoctorWeeklySchedulesVO)
        object.__setattr__(vo, "schedules", {"monday": "not-a-list"})

        with pytest.raises(ValueError, match="must be a list"):
            vo.validate()

    def test_validate_raises_for_uppercase_day_name(self):
        """Should raise ValueError for day names in uppercase (case-sensitive)."""
        with pytest.raises(ValueError, match="Invalid day"):
            DoctorWeeklySchedulesVO(schedules={"Monday": [_morning_slot()]})


# ─────────────────────── validate – overlapping slots ───────────────────────


class TestDoctorWeeklySchedulesVOOverlap:
    """Tests for overlapping-slot detection."""

    def test_validate_passes_for_non_overlapping_slots(self):
        """Should not raise when slots do not overlap."""
        vo = DoctorWeeklySchedulesVO(
            schedules={"monday": [_morning_slot(), _afternoon_slot()]}
        )

        vo.validate()  # must not raise

    def test_validate_raises_for_fully_overlapping_slots(self):
        """Should raise ValueError when two slots are identical."""
        slot = _morning_slot()

        with pytest.raises(ValueError, match="Overlapping slots"):
            DoctorWeeklySchedulesVO(schedules={"monday": [slot, slot]})

    def test_validate_raises_for_partially_overlapping_slots(self):
        """Should raise ValueError when one slot starts inside another."""
        slot_a = _slot(time(8, 0), time(10, 0), 60)
        slot_b = _slot(time(9, 0), time(11, 0), 60)

        with pytest.raises(ValueError, match="Overlapping slots"):
            DoctorWeeklySchedulesVO(schedules={"monday": [slot_a, slot_b]})

    def test_validate_passes_for_adjacent_slots(self):
        """Should not raise when the end of one slot equals the start of the next."""
        slot_a = _slot(time(8, 0), time(10, 0), 60)
        slot_b = _slot(time(10, 0), time(12, 0), 60)

        vo = DoctorWeeklySchedulesVO(schedules={"monday": [slot_a, slot_b]})

        vo.validate()  # must not raise

    def test_validate_passes_for_single_slot(self):
        """Should not raise when a day has only one slot (no overlap possible)."""
        vo = DoctorWeeklySchedulesVO(schedules={"monday": [_morning_slot()]})

        vo.validate()  # must not raise

    def test_validate_overlap_is_checked_per_day(self):
        """Overlapping slots on different days should be checked independently."""
        slot = _slot(time(8, 0), time(10, 0), 60)

        # Same slot on two different days — should NOT raise
        vo = DoctorWeeklySchedulesVO(
            schedules={
                "monday": [slot],
                "tuesday": [slot],
            }
        )

        vo.validate()  # must not raise

    def test_validate_raises_for_overlapping_slots_regardless_of_order(self):
        """Overlap detection should work even when slots are given in reverse order."""
        slot_a = _slot(time(9, 0), time(11, 0), 60)
        slot_b = _slot(time(8, 0), time(10, 0), 60)  # starts before slot_a but overlaps

        with pytest.raises(ValueError, match="Overlapping slots"):
            DoctorWeeklySchedulesVO(schedules={"monday": [slot_a, slot_b]})

    def test_validate_passes_for_three_non_overlapping_slots(self):
        """Should not raise with three consecutive non-overlapping slots."""
        slots = [
            _slot(time(8, 0), time(10, 0), 60),
            _slot(time(10, 0), time(13, 0), 60),
            _slot(time(14, 0), time(17, 0), 60),
        ]

        vo = DoctorWeeklySchedulesVO(schedules={"monday": slots})

        vo.validate()  # must not raise


# ─────────────────────────── to_dict ────────────────────────────────────────


class TestDoctorWeeklySchedulesVOToDict:
    """Tests for DoctorWeeklySchedulesVO.to_dict()."""

    def test_to_dict_returns_a_dict(self):
        """to_dict must return a dict instance."""
        vo = DoctorWeeklySchedulesVO(schedules={"monday": [_morning_slot()]})

        result = vo.to_dict()

        assert isinstance(result, dict)

    def test_to_dict_contains_all_days_present_in_schedules(self):
        """to_dict must include every day key that was provided."""
        vo = DoctorWeeklySchedulesVO(
            schedules={
                "monday": [_morning_slot()],
                "friday": [_afternoon_slot()],
            }
        )

        result = vo.to_dict()

        assert "monday" in result
        assert "friday" in result

    def test_to_dict_day_value_is_a_list(self):
        """Each day value in the dict must be a list."""
        vo = DoctorWeeklySchedulesVO(schedules={"monday": [_morning_slot()]})

        result = vo.to_dict()

        assert isinstance(result["monday"], list)

    def test_to_dict_slot_entries_are_dicts(self):
        """Each slot inside a day list must be serialised as a dict."""
        vo = DoctorWeeklySchedulesVO(schedules={"monday": [_morning_slot()]})

        result = vo.to_dict()

        assert isinstance(result["monday"][0], dict)

    def test_to_dict_slot_contains_expected_keys(self):
        """Each serialised slot must contain start_time, end_time, slot_duration_minutes, is_available."""
        vo = DoctorWeeklySchedulesVO(schedules={"monday": [_morning_slot()]})

        slot_dict = vo.to_dict()["monday"][0]

        assert "start_time" in slot_dict
        assert "end_time" in slot_dict
        assert "slot_duration_minutes" in slot_dict
        assert "is_available" in slot_dict

    def test_to_dict_preserves_slot_values(self):
        """Slot values must be serialised correctly (times as ISO strings)."""
        slot = _slot(time(8, 0), time(12, 0), 60)
        vo = DoctorWeeklySchedulesVO(schedules={"monday": [slot]})

        slot_dict = vo.to_dict()["monday"][0]

        assert slot_dict["start_time"] == "08:00"
        assert slot_dict["end_time"] == "12:00"
        assert slot_dict["slot_duration_minutes"] == 60
        assert slot_dict["is_available"] is True

    def test_to_dict_with_multiple_slots_per_day(self):
        """to_dict must include all slots for a day with multiple entries."""
        vo = DoctorWeeklySchedulesVO(
            schedules={"monday": [_morning_slot(), _afternoon_slot()]}
        )

        result = vo.to_dict()

        assert len(result["monday"]) == 2

    def test_to_dict_with_empty_slots_list(self):
        """to_dict must map a day with no slots to an empty list."""
        vo = DoctorWeeklySchedulesVO(schedules={"monday": []})

        result = vo.to_dict()

        assert result["monday"] == []

    def test_to_dict_with_all_seven_days(self):
        """to_dict must include all seven days when all are present."""
        all_days = {
            day: [_morning_slot()]
            for day in [
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            ]
        }
        vo = DoctorWeeklySchedulesVO(schedules=all_days)

        result = vo.to_dict()

        assert len(result) == 7
