"""Unit tests for TemplateNameVO."""

import pytest

from src.shared.domain.value_objects.template_name_vo import TemplateNameVO


class TestTemplateNameVO:
    """Unit tests for TemplateNameVO."""

    def test_should_create_template_name_vo_successfully(self):
        """Should create TemplateNameVO successfully with valid name."""
        name = "valid_template_name"
        vo = TemplateNameVO(name=name)
        assert vo.name == name

    def test_should_raise_value_error_for_empty_name(self):
        """Should raise ValueError for empty template name."""
        with pytest.raises(ValueError) as exc_info:
            TemplateNameVO(name="")
        assert "Template name cannot be empty or whitespace" in str(exc_info.value)

    def test_should_raise_value_error_for_whitespace_name(self):
        """Should raise ValueError for template name with only whitespace."""
        with pytest.raises(ValueError) as exc_info:
            TemplateNameVO(name="   ")
        assert "Template name cannot be empty or whitespace" in str(exc_info.value)
