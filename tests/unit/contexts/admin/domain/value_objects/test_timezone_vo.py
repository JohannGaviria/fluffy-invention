"""Unit tests for TimezoneVO."""

from dataclasses import FrozenInstanceError

import pytest

from src.contexts.admin.domain.value_objects.timezone_vo import TimezoneVO


class TestTimezoneVOCreation:
    """Tests for TimezoneVO creation and field access."""

    def test_should_create_successfully_with_utc(self):
        """Should create TimezoneVO with UTC timezone."""
        vo = TimezoneVO(timezone="UTC")

        assert vo.timezone == "UTC"

    def test_should_create_successfully_with_america_new_york(self):
        """Should create TimezoneVO with America/New_York."""
        vo = TimezoneVO(timezone="America/New_York")

        assert vo.timezone == "America/New_York"

    def test_should_create_successfully_with_america_bogota(self):
        """Should create TimezoneVO with America/Bogota."""
        vo = TimezoneVO(timezone="America/Bogota")

        assert vo.timezone == "America/Bogota"

    def test_should_create_successfully_with_europe_london(self):
        """Should create TimezoneVO with Europe/London."""
        vo = TimezoneVO(timezone="Europe/London")

        assert vo.timezone == "Europe/London"

    def test_should_create_successfully_with_asia_tokyo(self):
        """Should create TimezoneVO with Asia/Tokyo."""
        vo = TimezoneVO(timezone="Asia/Tokyo")

        assert vo.timezone == "Asia/Tokyo"

    def test_should_be_frozen_dataclass(self):
        """Should be immutable (frozen dataclass)."""
        vo = TimezoneVO(timezone="UTC")

        with pytest.raises(FrozenInstanceError):
            vo.timezone = "America/New_York"

    def test_should_create_with_various_valid_timezones(self):
        """Should create TimezoneVO with a range of valid IANA timezones."""
        valid_timezones = [
            "UTC",
            "America/Bogota",
            "America/New_York",
            "America/Los_Angeles",
            "America/Sao_Paulo",
            "Europe/London",
            "Europe/Paris",
            "Asia/Tokyo",
            "Australia/Sydney",
        ]

        for tz in valid_timezones:
            vo = TimezoneVO(timezone=tz)
            assert vo.timezone == tz


class TestTimezoneVOPostInit:
    """Tests for TimezoneVO.__post_init__ validation (runs at construction)."""

    def test_raises_value_error_for_invalid_timezone(self):
        """Should raise ValueError when timezone string is not a valid IANA zone."""
        with pytest.raises(ValueError, match="Invalid timezone"):
            TimezoneVO(timezone="Invalid/Zone")

    def test_raises_value_error_for_random_string(self):
        """Should raise ValueError for a completely random string."""
        with pytest.raises(ValueError, match="Invalid timezone"):
            TimezoneVO(timezone="not_a_timezone")

    def test_raises_value_error_for_lowercase_utc(self):
        """Should raise ValueError for 'utc' (IANA zones are case-sensitive)."""
        with pytest.raises(ValueError):
            TimezoneVO(timezone="utc")

    def test_raises_value_error_for_partial_timezone(self):
        """Should raise ValueError for a partial timezone string."""
        with pytest.raises(ValueError, match="Invalid timezone"):
            TimezoneVO(timezone="America")


class TestTimezoneVOValue:
    """Tests for TimezoneVO.value method."""

    def test_value_returns_timezone_string(self):
        """value() must return the same string as the timezone field."""
        vo = TimezoneVO(timezone="UTC")

        assert vo.value() == "UTC"

    def test_value_equals_timezone_attribute(self):
        """value() and timezone must always be equal."""
        for tz in ["UTC", "America/Bogota", "America/New_York", "Europe/London"]:
            vo = TimezoneVO(timezone=tz)
            assert vo.value() == vo.timezone

    def test_value_returns_correct_string_for_america_bogota(self):
        """value() must return 'America/Bogota' when that timezone is set."""
        vo = TimezoneVO(timezone="America/Bogota")

        assert vo.value() == "America/Bogota"

    def test_value_returns_correct_string_for_asia_tokyo(self):
        """value() must return 'Asia/Tokyo' when that timezone is set."""
        vo = TimezoneVO(timezone="Asia/Tokyo")

        assert vo.value() == "Asia/Tokyo"

    def test_value_is_a_string(self):
        """value() must return a str instance."""
        vo = TimezoneVO(timezone="UTC")

        assert isinstance(vo.value(), str)


class TestTimezoneVOValidate:
    """Tests for TimezoneVO.validate()."""

    def test_validate_passes_for_valid_timezone(self):
        """Should not raise when timezone is valid."""
        vo = TimezoneVO(timezone="UTC")

        vo.validate()  # must not raise

    def test_validate_raises_for_empty_string(self):
        """Should raise ValueError when timezone is empty."""
        # Empty string fails __post_init__ first (ZoneInfoNotFoundError → ValueError).
        # We bypass __post_init__ by using object.__setattr__ on the frozen instance
        # to directly test validate().
        vo = TimezoneVO.__new__(TimezoneVO)
        object.__setattr__(vo, "timezone", "")

        with pytest.raises(ValueError, match="Timezone cannot be empty"):
            vo.validate()

    def test_validate_raises_for_whitespace_only(self):
        """Should raise ValueError when timezone is only whitespace."""
        vo = TimezoneVO.__new__(TimezoneVO)
        object.__setattr__(vo, "timezone", "   ")

        with pytest.raises(ValueError, match="Timezone cannot be empty"):
            vo.validate()

    def test_validate_passes_for_america_bogota(self):
        """Should not raise when timezone is America/Bogota."""
        vo = TimezoneVO(timezone="America/Bogota")

        vo.validate()  # must not raise
