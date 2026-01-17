"""This module contains the TemplateRendererServicePort abstract class."""

from abc import ABC, abstractmethod


class TemplateRendererServicePort(ABC):
    """Abstract port for rendering templates."""

    @abstractmethod
    def render(self, template_name: str, context: dict) -> str:
        """Render a template with the given context.

        Args:
            template_name (str): The name of the template to render.
            context (dict): The context data to populate the template.

        Returns:
            str: The rendered template as a string.
        """
        pass
