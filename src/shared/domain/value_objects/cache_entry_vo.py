"""This module contains the CacheEntryVO value object definition."""

from dataclasses import dataclass
from typing import Generic, TypeVar

from src.shared.domain.value_objects.cache_key_vo import CacheKeyVO
from src.shared.domain.value_objects.cache_ttl_vo import CacheTTLVO
from src.shared.domain.value_objects.cache_value_vo import CacheValueVO
from src.shared.domain.value_objects.value_object import BaseValueObject

# Define a type variable for CacheValueVO
CacheValueType = TypeVar("CacheValueType", bound=CacheValueVO)


@dataclass(frozen=True)
class CacheEntryVO(BaseValueObject, Generic[CacheValueType]):  # noqa: UP046
    """Value object representing a cache entry."""

    key: CacheKeyVO
    ttl: CacheTTLVO
    value: CacheValueType

    def validate(self) -> None:
        """Validate the cache entry components.

        Raises:
            ValueError: If any component is invalid.
        """
        if self.value is None:
            raise ValueError("Cache value cannot be None")
