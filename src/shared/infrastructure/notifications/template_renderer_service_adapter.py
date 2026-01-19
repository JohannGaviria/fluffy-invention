"""This module contains the TemplateRendererServiceAdapter class which implements."""

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.shared.domain.template_renderer_service_port import TemplateRendererServicePort


class TemplateRendererServiceAdapter(TemplateRendererServicePort):
    """Adapter for rendering templates using Jinja2."""

    def __init__(self, templates_path: str) -> None:
        """Initializes the template renderer with the given templates path.

        Args:
            templates_path (str): The file system path to the templates directory.
        """
        self.env = Environment(
            loader=FileSystemLoader(templates_path),
            autoescape=select_autoescape(["html"]),
        )

    def render(self, template_name: str, context: dict) -> str:
        """Renders a template with the given context.

        Args:
            template_name (str): The name of the template file.
            context (dict): The context to render the template with.

        Returns:
            str: The rendered template as a string.
        """
        template = self.env.get_template(template_name)
        return template.render(**context)
