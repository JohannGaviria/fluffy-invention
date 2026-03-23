"""This module contains the DaysOfWeekEnum class, which represents the days of the week as an enumeration."""

from enum import Enum


class DaysOfWeekEnum(str, Enum):
    """Enum representing the days of the week.

    Attributes:
        MONDAY (str): Monday.
        TUESDAY (str): Tuesday.
        WEDNESDAY (str): Wednesday.
        THURSDAY (str): Thursday.
        FRIDAY (str): Friday.
        SATURDAY (str): Saturday.
        SUNDAY (str): Sunday.
    """

    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
