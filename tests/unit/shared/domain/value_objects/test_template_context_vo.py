"""Unit tests for TemplateContextVO."""

from dataclasses import dataclass

import pytest

from src.shared.domain.value_objects.template_context_vo import TemplateContextVO


@dataclass(frozen=True)
class MockTemplateContextVO(TemplateContextVO):
    """Mock implementation of TemplateContextVO for testing."""

    data: str

    def to_dict(self) -> dict:
        return {"data": self.data}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data=data["data"])

    def validate(self) -> None:
        if not isinstance(self.data, str):
            raise ValueError("Data must be a string.")


class TestTemplateContextVO:
    """Unit tests for TemplateContextVO."""

    def test_should_create_mock_template_context_vo_successfully(self):
        """Should create MockTemplateContextVO successfully with valid data."""
        data = "valid_data"
        vo = MockTemplateContextVO(data=data)
        assert vo.data == data

    def test_should_convert_to_dict_successfully(self):
        """Should convert MockTemplateContextVO to dictionary successfully."""
        data = "valid_data"
        vo = MockTemplateContextVO(data=data)
        result = vo.to_dict()
        assert result == {"data": data}

    def test_should_create_from_dict_successfully(self):
        """Should create MockTemplateContextVO from dictionary successfully."""
        data = {"data": "valid_data"}
        vo = MockTemplateContextVO.from_dict(data)
        assert vo.data == data["data"]

    def test_should_raise_value_error_for_invalid_data(self):
        """Should raise ValueError for invalid data type."""
        with pytest.raises(ValueError) as exc_info:
            MockTemplateContextVO(data=123)  # Invalid data type
        assert "Data must be a string." in str(exc_info.value)

    def test_should_validate_during_from_dict(self):
        """Should validate during from_dict creation."""
        with pytest.raises(ValueError) as exc_info:
            MockTemplateContextVO.from_dict({"data": 123})  # Invalid data type
        assert "Data must be a string." in str(exc_info.value)
