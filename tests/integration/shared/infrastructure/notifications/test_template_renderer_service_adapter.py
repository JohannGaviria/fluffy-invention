"""Integration tests for TemplateRendererServiceAdapter."""

import os

import pytest

from src.shared.domain.value_objects.template_renderer_vo import (
    TemplateNameVO,
    TemplateRendererVO,
)
from src.shared.domain.value_objects.value_object import BaseValueObject
from src.shared.infrastructure.notifications.template_renderer_service_adapter import (
    TemplateRendererServiceAdapter,
)


class MockTemplateContextVO(BaseValueObject):
    """Mock implementation of TemplateContextVO for testing."""

    def __init__(self, data):
        """Initialization MockTemplateContextVO."""
        self.data = data

    def to_dict(self) -> dict:
        """Convert to dict."""
        return self.data

    def validate(self) -> None:
        """Validate."""
        pass


class TestTemplateRendererServiceAdapter:
    @pytest.fixture
    def template_renderer(self):
        templates_path = os.path.join(os.path.dirname(__file__), "templates")
        os.makedirs(templates_path, exist_ok=True)
        with open(os.path.join(templates_path, "test_template.html"), "w") as f:
            f.write("<h1>{{ title }}</h1><p>{{ content }}</p>")

        yield TemplateRendererServiceAdapter(templates_path, MockTemplateContextVO)

        # Cleanup
        os.remove(os.path.join(templates_path, "test_template.html"))
        os.rmdir(templates_path)

    def test_render_template_successfully(self, template_renderer):
        """Should render a template successfully with valid context."""
        template_name = TemplateNameVO("test_template.html")
        context = MockTemplateContextVO(data={"title": "Hello", "content": "World"})
        template_vo = TemplateRendererVO(template_name=template_name, context=context)

        result = template_renderer.render(template_vo)

        assert "<h1>Hello</h1>" in result
        assert "<p>World</p>" in result
