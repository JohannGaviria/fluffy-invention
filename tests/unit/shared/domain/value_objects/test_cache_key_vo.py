"""Unit tests for CacheKeyVO."""

import pytest

from src.shared.domain.value_objects.cache_key_vo import CacheKeyVO


class TestCacheKeyVO:
    """Unit tests for CacheKeyVO."""

    def test_should_create_cache_key_vo_successfully(self):
        """Should create CacheKeyVO successfully with valid key."""
        key = "cache:user:123"
        vo = CacheKeyVO(key=key)
        assert vo.key == key

    def test_should_raise_value_error_for_empty_key(self):
        """Should raise ValueError for empty cache key."""
        with pytest.raises(ValueError) as exc_info:
            CacheKeyVO(key="")
        assert "Cache key cannot be empty" in str(exc_info.value)

    def test_should_raise_value_error_for_invalid_format(self):
        """Should raise ValueError for invalid cache key format."""
        invalid_key = "invalid_key"
        with pytest.raises(ValueError) as exc_info:
            CacheKeyVO(key=invalid_key)
        assert "Invalid cache key format" in str(exc_info.value)

    def test_should_raise_value_error_for_key_too_long(self):
        """Should raise ValueError for cache key exceeding max length."""
        long_key = "cache:abc:" + "a" * 245
        with pytest.raises(ValueError) as exc_info:
            CacheKeyVO(key=long_key)
        assert "Cache key too long (max 250 characters)" in str(exc_info.value)
