"""This module contains unit tests for TemplateRendererVO."""

from dataclasses import FrozenInstanceError, dataclass

import pytest

from src.shared.domain.value_objects.template_renderer_vo import TemplateRendererVO
from src.shared.domain.value_objects.value_object import BaseValueObject


# Mock implementations for testing
@dataclass(frozen=True)
class MockTemplateNameVO(BaseValueObject):
    """Mock TemplateNameVO for testing."""

    value: str

    def validate(self) -> None:
        """Validate the mock TemplateNameVO."""
        if not isinstance(self.value, str) or not self.value:
            raise ValueError("value must be a non-empty string")


@dataclass(frozen=True)
class MockTemplateContextVO(BaseValueObject):
    """Mock TemplateContextVO for testing."""

    value: tuple

    def validate(self) -> None:
        """Validate the mock TemplateContextVO."""
        if not isinstance(self.value, tuple):
            raise ValueError("value must be a tuple")


@dataclass(frozen=True)
class AnotherMockTemplateContextVO(BaseValueObject):
    """Another mock TemplateContextVO for testing."""

    data: str

    def validate(self) -> None:
        """Validate the mock TemplateContextVO."""
        if not isinstance(self.data, str):
            raise ValueError("data must be a string")


class TestTemplateRendererVO:
    """Unit tests for TemplateRendererVO."""

    def test_should_create_template_renderer_vo_successfully(self):
        """Should create TemplateRendererVO successfully with valid data."""
        template_name = MockTemplateNameVO(value="test_template.html")
        context = MockTemplateContextVO(value=("key", "value"))

        vo = TemplateRendererVO(template_name=template_name, context=context)

        assert vo.template_name == template_name
        assert vo.context == context

    def test_should_validate_context_not_none_success(self):
        """Should validate successfully when context is not None."""
        template_name = MockTemplateNameVO(value="test_template.html")
        context = MockTemplateContextVO(value=("key", "value"))

        vo = TemplateRendererVO(template_name=template_name, context=context)

        # No exception should be raised
        assert vo is not None

    def test_should_raise_value_error_when_context_is_none(self):
        """Should raise ValueError when context is None."""
        template_name = MockTemplateNameVO(value="test_template.html")

        with pytest.raises(ValueError) as exc_info:
            TemplateRendererVO(template_name=template_name, context=None)

        assert "Context cannot be None" in str(exc_info.value)

    def test_should_raise_value_error_when_template_name_is_none(self):
        """Should raise ValueError when template_name is None."""
        context = MockTemplateContextVO(value=("key", "value"))

        with pytest.raises(ValueError) as exc_info:
            TemplateRendererVO(template_name=None, context=context)

        assert "Template name cannot be None" in str(exc_info.value)

    def test_should_raise_value_error_when_both_are_none(self):
        """Should raise ValueError when both template_name and context are None."""
        with pytest.raises(ValueError) as exc_info:
            TemplateRendererVO(template_name=None, context=None)

        assert "template name cannot be none" in str(exc_info.value).lower()

    def test_should_work_with_different_context_types(self):
        """Should work with different types of TemplateContextVO implementations."""
        template_name = MockTemplateNameVO(value="test_template.html")

        # Test with first context type
        context1 = MockTemplateContextVO(value=("key", "value"))
        vo1 = TemplateRendererVO(template_name=template_name, context=context1)
        assert vo1.context == context1

        # Test with second context type
        context2 = AnotherMockTemplateContextVO(data="test_data")
        vo2 = TemplateRendererVO(template_name=template_name, context=context2)
        assert vo2.context == context2

    def test_should_be_immutable(self):
        """TemplateRendererVO should be immutable (frozen dataclass)."""
        template_name = MockTemplateNameVO(value="test_template.html")
        context = MockTemplateContextVO(value=("key", "value"))

        vo = TemplateRendererVO(template_name=template_name, context=context)

        # Verify immutability by trying to modify attributes
        with pytest.raises(FrozenInstanceError):
            vo.template_name = MockTemplateNameVO(value="another.html")

        with pytest.raises(FrozenInstanceError):
            vo.context = MockTemplateContextVO(value=("another", "value"))

    def test_should_have_correct_generic_type(self):
        """Should correctly handle generic type parameter."""
        template_name = MockTemplateNameVO(value="test_template.html")
        context = MockTemplateContextVO(value=("key", "value"))

        # Explicitly specify the generic type
        vo: TemplateRendererVO[MockTemplateContextVO] = TemplateRendererVO(  # type: ignore[type-var]
            template_name=template_name, context=context
        )

        # Type checking should pass
        assert isinstance(vo.context, MockTemplateContextVO)

    def test_should_compare_equal_for_same_values(self):
        """Two TemplateRendererVOs with same values should be equal."""
        template_name = MockTemplateNameVO(value="test_template.html")
        context = MockTemplateContextVO(value=("key", "value"))

        vo1 = TemplateRendererVO(template_name=template_name, context=context)
        vo2 = TemplateRendererVO(template_name=template_name, context=context)

        assert vo1 == vo2
        assert hash(vo1) == hash(vo2)

    def test_should_compare_not_equal_for_different_values(self):
        """Two TemplateRendererVOs with different values should not be equal."""
        template_name1 = MockTemplateNameVO(value="template1.html")
        template_name2 = MockTemplateNameVO(value="template2.html")
        context = MockTemplateContextVO(value=("key", "value"))

        vo1 = TemplateRendererVO(template_name=template_name1, context=context)
        vo2 = TemplateRendererVO(template_name=template_name2, context=context)

        assert vo1 != vo2

    def test_should_compare_not_equal_for_different_contexts(self):
        """Two TemplateRendererVOs with different contexts should not be equal."""
        template_name = MockTemplateNameVO(value="template.html")
        context1 = MockTemplateContextVO(value=("key1", "value1"))
        context2 = MockTemplateContextVO(value=("key2", "value2"))

        vo1 = TemplateRendererVO(template_name=template_name, context=context1)
        vo2 = TemplateRendererVO(template_name=template_name, context=context2)

        assert vo1 != vo2

    def test_should_validate_inner_value_objects(self):
        """Should validate the inner value objects during creation."""
        # This should fail because MockTemplateNameVO validates empty string
        with pytest.raises(ValueError) as exc_info:
            bad_template_name = MockTemplateNameVO(value="")
            context = MockTemplateContextVO(value=("key", "value"))
            TemplateRendererVO(template_name=bad_template_name, context=context)

        assert "value must be a non-empty string" in str(exc_info.value)

    def test_should_validate_invalid_context_value_object(self):
        """Should validate when context value object is invalid."""
        template_name = MockTemplateNameVO(value="test_template.html")

        with pytest.raises(ValueError) as exc_info:
            bad_context = MockTemplateContextVO(
                value={"key": "value"}
            )  # dict instead of tuple
            TemplateRendererVO(template_name=template_name, context=bad_context)

        assert "value must be a tuple" in str(exc_info.value)

    def test_string_representation(self):
        """Should have a proper string representation."""
        template_name = MockTemplateNameVO(value="test_template.html")
        context = MockTemplateContextVO(value=("key", "value"))

        vo = TemplateRendererVO(template_name=template_name, context=context)

        repr_str = repr(vo)
        assert "TemplateRendererVO" in repr_str
        assert "test_template.html" in repr_str

        str_str = str(vo)
        assert "TemplateRendererVO" in str_str
