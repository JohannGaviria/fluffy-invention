"""This module contains unit tests for BaseValueObject."""

from dataclasses import dataclass

import pytest

from src.shared.domain.value_objects.value_object import BaseValueObject


@dataclass(frozen=True)
class GoodVO(BaseValueObject):
    """A concrete implementation of BaseValueObject for testing."""

    value: int

    def validate(self) -> None:
        """Validate the concrete implementation."""
        if not isinstance(self.value, int):
            raise ValueError("value must be int")


@dataclass(frozen=True)
class BadVO(BaseValueObject):
    """A concrete implementation of BaseValueObject for testing."""

    value: int

    def validate(self) -> None:
        """Validate the concrete implementation."""
        raise ValueError("invalid")


class TestBaseValueObject:
    """Unit tests for BaseValueObject."""

    def test_should_post_init_calls_validate_success(self):
        """Should call validate successfully."""
        vo = GoodVO(value=1)
        assert vo.value == 1

    def test_should_post_init_calls_validate_failure(self):
        """Should call validate failure."""
        with pytest.raises(ValueError):
            BadVO(value=1)
