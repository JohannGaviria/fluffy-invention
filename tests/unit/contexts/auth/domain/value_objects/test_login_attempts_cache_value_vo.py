"""Unit tests for LoginAttemptsCacheValueVO."""

from dataclasses import FrozenInstanceError

import pytest

from src.contexts.auth.domain.value_objects.login_attempts_cache_value_vo import (
    LoginAttemptsCacheValueVO,
)


class TestLoginAttemptsCacheValueVO:
    """Unit tests for LoginAttemptsCacheValueVO."""

    def test_should_create_login_attempts_cache_value_vo_successfully(self):
        """Should create LoginAttemptsCacheValueVO successfully with valid data."""
        vo = LoginAttemptsCacheValueVO(attempt=5)
        assert vo.attempt == 5

    def test_should_create_with_zero_attempts(self):
        """Should create LoginAttemptsCacheValueVO with zero attempts."""
        vo = LoginAttemptsCacheValueVO(attempt=0)
        assert vo.attempt == 0

    def test_should_raise_value_error_for_negative_attempts(self):
        """Should raise ValueError for negative attempts."""
        with pytest.raises(ValueError) as exc_info:
            LoginAttemptsCacheValueVO(attempt=-1)
        assert "Attempts cannot be negative" in str(exc_info.value)

    def test_should_raise_value_error_for_attempts_exceeding_max(self):
        """Should raise ValueError for attempts exceeding maximum limit."""
        with pytest.raises(ValueError) as exc_info:
            LoginAttemptsCacheValueVO(attempt=101)
        assert "Attempts exceed maximum limit" in str(exc_info.value)

    def test_should_convert_to_dict_successfully(self):
        """Should convert LoginAttemptsCacheValueVO to dictionary successfully."""
        vo = LoginAttemptsCacheValueVO(attempt=3)
        result = vo.to_dict()
        assert result == {"attempt": 3}

    def test_should_create_from_dict_successfully(self):
        """Should create LoginAttemptsCacheValueVO from dictionary successfully."""
        data = {"attempt": 7}
        vo = LoginAttemptsCacheValueVO.from_dict(data)
        assert vo.attempt == 7

    def test_should_increment_attempts_successfully(self):
        """Should increment attempts and return new instance."""
        vo = LoginAttemptsCacheValueVO(attempt=3)
        incremented = vo.increment()

        assert incremented.attempt == 4
        assert vo.attempt == 3  # Original should be unchanged (immutable)

    def test_should_increment_from_zero(self):
        """Should increment from zero attempts."""
        vo = LoginAttemptsCacheValueVO(attempt=0)
        incremented = vo.increment()

        assert incremented.attempt == 1

    def test_should_create_initial_instance(self):
        """Should create initial instance with zero attempts."""
        vo = LoginAttemptsCacheValueVO.initial()
        assert vo.attempt == 0

    def test_should_be_frozen_dataclass(self):
        """Should be immutable (frozen dataclass)."""
        vo = LoginAttemptsCacheValueVO(attempt=5)

        with pytest.raises(FrozenInstanceError):
            vo.attempt = 10

    def test_should_validate_on_creation_from_dict(self):
        """Should validate when creating from dictionary."""
        with pytest.raises(ValueError) as exc_info:
            LoginAttemptsCacheValueVO.from_dict({"attempt": -5})
        assert "Attempts cannot be negative" in str(exc_info.value)

    def test_should_validate_on_increment(self):
        """Should validate after increment."""
        vo = LoginAttemptsCacheValueVO(attempt=100)

        with pytest.raises(ValueError) as exc_info:
            vo.increment()
        assert "Attempts exceed maximum limit" in str(exc_info.value)
