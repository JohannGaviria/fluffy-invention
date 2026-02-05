"""Unit tests for CacheEntryVO."""

import pytest

from src.shared.domain.value_objects.cache_entry_vo import CacheEntryVO
from src.shared.domain.value_objects.cache_key_vo import CacheKeyVO
from src.shared.domain.value_objects.cache_ttl_vo import CacheTTLVO
from src.shared.domain.value_objects.cache_value_vo import CacheValueVO


class MockCacheValueVO(CacheValueVO):
    """Mock implementation of CacheValueVO for testing."""

    def __init__(self, data):
        """Initialize the MockCacheValueVO."""
        self.data = data

    def to_dict(self) -> dict:
        """Convert into a dict."""
        return {"data": self.data}

    @classmethod
    def from_dict(cls, data: dict):
        """Convert from dict."""
        return cls(data=data["data"])

    def validate(self) -> None:
        """Validate."""
        if not isinstance(self.data, str):
            raise ValueError("Data must be a string.")


class TestCacheEntryVO:
    """Unit tests for CacheEntryVO."""

    def test_should_create_cache_entry_vo_successfully(self):
        """Should create CacheEntryVO successfully with valid components."""
        key = CacheKeyVO(key="cache:user:123")
        ttl = CacheTTLVO(seconds=3600)
        value = MockCacheValueVO(data="valid_data")
        entry = CacheEntryVO(key=key, ttl=ttl, value=value)

        assert entry.key == key
        assert entry.ttl == ttl
        assert entry.value == value

    def test_should_raise_value_error_for_none_value(self):
        """Should raise ValueError when cache value is None."""
        key = CacheKeyVO(key="cache:user:123")
        ttl = CacheTTLVO(seconds=3600)

        with pytest.raises(ValueError) as exc_info:
            CacheEntryVO(key=key, ttl=ttl, value=None)
        assert "Cache value cannot be None" in str(exc_info.value)
