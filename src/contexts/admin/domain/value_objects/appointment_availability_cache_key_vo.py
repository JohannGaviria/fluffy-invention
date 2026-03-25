"""This module contains the value object for the appointment availability cache key."""

from dataclasses import dataclass

from src.shared.domain.constants.cache_keys_constant import (
    APPOINTMENT_AVAILABILITY_KEY_PREFIX,
)
from src.shared.domain.value_objects.cache_key_vo import CacheKeyVO


@dataclass(frozen=True)
class AppointmentAvailabilityCacheKeyVO(CacheKeyVO):
    """Value object representing a cache key for appointment availability in the admin context."""

    @classmethod
    def from_doctor_id(cls, doctor_id: str) -> "AppointmentAvailabilityCacheKeyVO":
        """Create an instance of AppointmentAvailabilityCacheKeyVO from a doctor ID.

        Args:
            doctor_id (str): The ID of the doctor for which to create the cache key.

        Returns:
            AppointmentAvailabilityCacheKeyVO: An instance of the cache key value object
                with the key formatted for appointment availability caching.
        """
        key = f"{APPOINTMENT_AVAILABILITY_KEY_PREFIX}:{doctor_id}"
        return cls(key=key)
