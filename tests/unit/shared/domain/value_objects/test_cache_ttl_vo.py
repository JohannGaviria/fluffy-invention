"""Unit tests for CacheTTLVO."""

import pytest

from src.shared.domain.value_objects.cache_ttl_vo import CacheTTLVO


class TestCacheTTLVO:
    """Unit tests for CacheTTLVO."""

    def test_should_create_cache_ttl_vo_successfully(self):
        """Should create CacheTTLVO successfully with valid seconds."""
        ttl = 3600
        vo = CacheTTLVO(seconds=ttl)
        assert vo.seconds == ttl

    def test_should_raise_value_error_for_negative_ttl(self):
        """Should raise ValueError for negative TTL."""
        with pytest.raises(ValueError) as exc_info:
            CacheTTLVO(seconds=-1)
        assert "TTL must be positive" in str(exc_info.value)

    def test_should_raise_value_error_for_ttl_exceeding_max(self):
        """Should raise ValueError for TTL exceeding maximum allowed value."""
        with pytest.raises(ValueError) as exc_info:
            CacheTTLVO(seconds=86400 * 31)  # More than 30 days
        assert "TTL too long (max 30 days)" in str(exc_info.value)

    def test_should_create_cache_ttl_vo_from_minutes(self):
        """Should create CacheTTLVO from minutes successfully."""
        minutes = 60
        vo = CacheTTLVO.from_minutes(minutes)
        assert vo.seconds == 3600

    def test_should_convert_cache_ttl_vo_to_minutes(self):
        """Should convert CacheTTLVO to minutes successfully."""
        ttl = 3600
        vo = CacheTTLVO(seconds=ttl)
        assert vo.to_minutes() == 60
