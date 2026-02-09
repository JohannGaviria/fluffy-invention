"""Integration tests for RedisCacheServiceAdapter."""

import json
from unittest.mock import ANY, MagicMock

import pytest
from redis import RedisError

from src.shared.domain.value_objects.cache_entry_vo import CacheEntryVO
from src.shared.domain.value_objects.cache_key_vo import CacheKeyVO
from src.shared.domain.value_objects.cache_ttl_vo import CacheTTLVO
from src.shared.domain.value_objects.cache_value_vo import CacheValueVO
from src.shared.infrastructure.cache.redis_cache_service_adapter import (
    RedisCacheServiceAdapter,
)
from src.shared.infrastructure.logging.logger import Logger


class MockCacheValueVO(CacheValueVO):
    def __init__(self, data):
        """Initialization MockCacheValueVO."""
        self.data = data

    def to_dict(self) -> dict:
        """Convert to dict."""
        return {"data": self.data}

    @classmethod
    def from_dict(cls, data: dict):
        """Convert from dict."""
        return cls(data=data["data"])

    def validate(self) -> None:
        """Validate."""
        pass


class TestsRedisCacheServiceAdapter:
    @pytest.fixture
    def redis_client_mock(self):
        redis_mock = MagicMock()
        redis_mock.get_client = MagicMock(return_value=redis_mock)
        redis_mock.get = MagicMock()
        redis_mock.setex = MagicMock()
        redis_mock.delete = MagicMock()
        return redis_mock

    @pytest.fixture
    def logger_mock(self):
        return MagicMock(spec=Logger)

    @pytest.fixture
    def redis_cache_service_adapter(self, redis_client_mock, logger_mock):
        return RedisCacheServiceAdapter(
            redis_client=redis_client_mock,
            logger=logger_mock,
            value_class=MockCacheValueVO,
        )

    # ---------- GET ----------

    def test_get_cache_hit(
        self, redis_cache_service_adapter, redis_client_mock, logger_mock
    ):
        key = CacheKeyVO(key="cache:user:123")
        redis_client_mock.get.return_value = '{"data": "cached_value"}'

        result = redis_cache_service_adapter.get(key)

        assert result.data == "cached_value"
        logger_mock.debug.assert_called_with(message="Cache GET hit", key=key.key)

    def test_get_cache_miss(
        self, redis_cache_service_adapter, redis_client_mock, logger_mock
    ):
        key = CacheKeyVO(key="cache:user:123")
        redis_client_mock.get.return_value = None

        result = redis_cache_service_adapter.get(key)

        assert result is None
        logger_mock.debug.assert_called_with(message="Cache GET miss", key=key.key)

    def test_get_json_decode_error(
        self, redis_cache_service_adapter, redis_client_mock, logger_mock
    ):
        key = CacheKeyVO(key="cache:user:123")
        redis_client_mock.get.return_value = "not-json"

        with pytest.raises(json.JSONDecodeError):
            redis_cache_service_adapter.get(key)

        logger_mock.error.assert_called_with(
            message="JSON decode failed for cache GET", key=key.key, error=ANY
        )

    def test_get_redis_error(
        self, redis_cache_service_adapter, redis_client_mock, logger_mock
    ):
        key = CacheKeyVO(key="cache:user:123")
        redis_client_mock.get.side_effect = RedisError("boom")

        with pytest.raises(RedisError):
            redis_cache_service_adapter.get(key)

        logger_mock.error.assert_called_with(
            message="Redis GET failed", key=key.key, error="boom"
        )

    def test_get_unexpected_error(
        self, redis_cache_service_adapter, redis_client_mock, logger_mock
    ):
        key = CacheKeyVO(key="cache:user:123")
        redis_client_mock.get.side_effect = RuntimeError("weird")

        with pytest.raises(RuntimeError):
            redis_cache_service_adapter.get(key)

        logger_mock.error.assert_called_with(
            message="Unexpected error during cache GET", key=key.key, error="weird"
        )

    # ---------- SET ----------

    def test_set_cache_value(
        self, redis_cache_service_adapter, redis_client_mock, logger_mock
    ):
        key = CacheKeyVO(key="cache:user:123")
        ttl = CacheTTLVO(seconds=3600)
        value = MockCacheValueVO(data="new_value")
        entry = CacheEntryVO(key=key, ttl=ttl, value=value)

        redis_cache_service_adapter.set(entry)

        redis_client_mock.setex.assert_called_once_with(
            key.key, ttl.seconds, '{"data": "new_value"}'
        )
        logger_mock.debug.assert_called_with(
            message="Cache SET successful", key=key.key, ttl=ttl.seconds
        )

    def test_set_serialization_error(self, redis_cache_service_adapter, logger_mock):
        key = CacheKeyVO(key="cache:test:1")
        ttl = CacheTTLVO(seconds=10)

        class BadValue(MockCacheValueVO):
            def to_dict(self):
                return {"data": object()}

        entry = CacheEntryVO(key=key, ttl=ttl, value=BadValue("x"))

        with pytest.raises(TypeError):
            redis_cache_service_adapter.set(entry)

        logger_mock.error.assert_called_with(
            message="Value serialization failed", key=key.key, error=ANY
        )

    def test_set_redis_error(
        self, redis_cache_service_adapter, redis_client_mock, logger_mock
    ):
        key = CacheKeyVO(key="cache:test:1")
        ttl = CacheTTLVO(seconds=10)
        value = MockCacheValueVO("x")
        entry = CacheEntryVO(key=key, ttl=ttl, value=value)

        redis_client_mock.setex.side_effect = RedisError("down")

        with pytest.raises(RedisError):
            redis_cache_service_adapter.set(entry)

        logger_mock.error.assert_called_with(
            message="Redis SET failed", key=key.key, error="down"
        )

    # ---------- DELETE ----------

    def test_delete_cache_key(
        self, redis_cache_service_adapter, redis_client_mock, logger_mock
    ):
        key = CacheKeyVO(key="cache:user:123")

        redis_cache_service_adapter.delete(key)

        redis_client_mock.delete.assert_called_once_with(key.key)
        logger_mock.debug.assert_called_with(
            message="Cache DELETE successful", key=key.key
        )

    def test_delete_redis_error(
        self, redis_cache_service_adapter, redis_client_mock, logger_mock
    ):
        key = CacheKeyVO(key="cache:test:1")
        redis_client_mock.delete.side_effect = RedisError("down")

        with pytest.raises(RedisError):
            redis_cache_service_adapter.delete(key)

        logger_mock.error.assert_called_with(
            message="Redis DELETE failed", key=key.key, error="down"
        )

    def test_delete_unexpected_error(
        self, redis_cache_service_adapter, redis_client_mock, logger_mock
    ):
        key = CacheKeyVO(key="cache:test:1")
        redis_client_mock.delete.side_effect = RuntimeError("weird")

        with pytest.raises(RuntimeError):
            redis_cache_service_adapter.delete(key)

        logger_mock.error.assert_called_with(
            message="Unexpected error during cache DELETE",
            key=key.key,
            error="weird",
        )
