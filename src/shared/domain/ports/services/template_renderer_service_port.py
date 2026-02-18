"""This module contains the TemplateRendererServicePort abstract class."""

from abc import ABC, abstractmethod
from typing import Generic

from src.shared.domain.value_objects.template_renderer_vo import (
    TemplateRendererContextType,
    TemplateRendererVO,
)


class TemplateRendererServicePort(ABC, Generic[TemplateRendererContextType]):  # noqa: UP046
    """Abstract port for rendering templates."""

    @abstractmethod
    def render(self, template: TemplateRendererVO[TemplateRendererContextType]) -> str:
        """Render a template with the given context.

        Args:
            template (TemplateRendererVO[TemplateRendererContextType]): The template and context to render.

        Returns:
            str: The rendered template as a string.
        """
        pass
