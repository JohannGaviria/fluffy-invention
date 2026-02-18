"""This module contains unit test for BaseEntity."""

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from src.shared.domain.entities.entity import BaseEntity


@dataclass
class ConcreteEntity(BaseEntity):
    """A concrete implementation of BaseEntity for testing."""

    pass


class TestBaseEntity:
    """Unit tests for BaseEntity."""

    def test_should_equality_same_id(self):
        """Should equality."""
        now = datetime.now(UTC)
        _id = uuid4()

        a = ConcreteEntity(id=_id, created_at=now, updated_at=now)
        b = ConcreteEntity(id=_id, created_at=now, updated_at=now)

        assert a == b

    def test_should_inequality_different_id(self):
        """Should inequality."""
        now = datetime.now(UTC)

        a = ConcreteEntity(id=uuid4(), created_at=now, updated_at=now)
        b = ConcreteEntity(id=uuid4(), created_at=now, updated_at=now)

        assert not (a == b)

    def test_inequality_different_class(self):
        """Should inequality."""

        @dataclass
        class OtherEntity(BaseEntity):
            """A concrete implementation of BaseEntity for testing."""

            pass

        now = datetime.now(UTC)
        _id = uuid4()

        a = ConcreteEntity(id=_id, created_at=now, updated_at=now)
        b = OtherEntity(id=_id, created_at=now, updated_at=now)

        assert not (a == b)

    def test_equality_with_none_id_returns_false(self):
        """Should return False if id is None."""
        now = datetime.now(UTC)

        a = ConcreteEntity(id=None, created_at=now, updated_at=now)
        b = ConcreteEntity(id=uuid4(), created_at=now, updated_at=now)

        assert not (a == b)
