"""Unit tests for CacheValueVO."""

from dataclasses import dataclass

import pytest

from src.shared.domain.value_objects.cache_value_vo import CacheValueVO


@dataclass(frozen=True)
class MockCacheValueVO(CacheValueVO):
    data: str

    def to_dict(self) -> dict:
        return {"data": self.data}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data=data["data"])

    def validate(self) -> None:
        if not isinstance(self.data, str):
            raise ValueError("Data must be a string.")


class TestCacheValueVO:
    """Unit tests for CacheValueVO."""

    def test_should_create_mock_cache_value_vo_successfully(self):
        """Should create MockCacheValueVO successfully with valid data."""
        data = "valid_data"
        vo = MockCacheValueVO(data=data)
        assert vo.data == data

    def test_should_convert_to_dict_successfully(self):
        """Should convert MockCacheValueVO to dictionary successfully."""
        data = "valid_data"
        vo = MockCacheValueVO(data=data)
        result = vo.to_dict()
        assert result == {"data": data}

    def test_should_create_from_dict_successfully(self):
        """Should create MockCacheValueVO from dictionary successfully."""
        data = {"data": "valid_data"}
        vo = MockCacheValueVO.from_dict(data)
        assert vo.data == data["data"]

    def test_should_raise_value_error_for_invalid_data(self):
        """Should raise ValueError for invalid data type."""
        with pytest.raises(ValueError) as exc_info:
            MockCacheValueVO(data=123)  # Invalid data type
        assert "Data must be a string." in str(exc_info.value)
