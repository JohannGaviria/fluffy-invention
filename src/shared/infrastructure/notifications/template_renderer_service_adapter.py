"""This module contains the TemplateRendererServiceAdapter class which implements."""

from typing import Generic

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.shared.domain.ports.services.template_renderer_service_port import (
    TemplateRendererServicePort,
)
from src.shared.domain.value_objects.template_renderer_vo import (
    TemplateRendererContextType,
    TemplateRendererVO,
)


class TemplateRendererServiceAdapter(
    TemplateRendererServicePort[TemplateRendererContextType],
    Generic[TemplateRendererContextType],  # noqa: UP046
):
    """Adapter for rendering templates using Jinja2."""

    def __init__(
        self, templates_path: str, value_class: type[TemplateRendererContextType]
    ) -> None:
        """Initializes the template renderer with the given templates path.

        Args:
            templates_path (str): The file system path to the templates directory.
            value_class (type[TemplateRendererContextType]): The class type for the context.
        """
        self.value_class = value_class
        self.env = Environment(
            loader=FileSystemLoader(templates_path),
            autoescape=select_autoescape(["html"]),
        )

    def render(self, template: TemplateRendererVO[TemplateRendererContextType]) -> str:
        """Renders a template with the given context.

        Args:
            template (TemplateRendererVO[TemplateRendererContextType]): The template and context to render.

        Returns:
            str: The rendered template as a string.
        """
        temp = self.env.get_template(template.template_name.name)
        return temp.render(**template.context.to_dict())
