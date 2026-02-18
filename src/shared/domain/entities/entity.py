"""This module contains the base class for entities in the domain layer."""

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class BaseEntity(ABC):
    """Base class for entities in the domain layer.

    Attributes:
        id (UUID): Unique identifier for the entity.
        created_at (datetime): Timestamp when the entity was created.
        updated_at (datetime): Timestamp when the entity was last updated.
    """

    id: UUID
    created_at: datetime
    updated_at: datetime
