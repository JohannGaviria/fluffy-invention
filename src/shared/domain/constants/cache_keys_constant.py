"""This module contains constants related to cache keys.

The constants defined here are used to standardize cache key formats across the application.
"""

# Key used to cache a doctor's appointment availability.
# Expected full format: "cache:clinical:appointment_availability:{doctor_id}"
APPOINTMENT_AVAILABILITY_KEY_PREFIX = "cache:admin:appointment_availability"
