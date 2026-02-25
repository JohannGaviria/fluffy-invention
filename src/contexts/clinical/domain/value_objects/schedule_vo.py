"""This module contains the Value Object for the Schedule entity."""

from dataclasses import dataclass

from src.contexts.clinical.domain.value_objects.schedule_day_vo import ScheduleDaysVO
from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class ScheduleVO(BaseValueObject):
    """Value object for the Schedule entity."""

    monday: list[ScheduleDaysVO] = []
    tuesday: list[ScheduleDaysVO] = []
    wednesday: list[ScheduleDaysVO] = []
    thursday: list[ScheduleDaysVO] = []
    friday: list[ScheduleDaysVO] = []
    saturday: list[ScheduleDaysVO] = []
    sunday: list[ScheduleDaysVO] = []
