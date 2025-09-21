import os

from backend.mailings.src.templates.contents import get_contents_folder
from backend.mailings.src.templates import exceptions as templates_exceptions

async def valid_template_name(template_name, language: str = "en"):
    templates_list = [
        os.path.splitext(file)[0]
        for file in os.listdir(get_contents_folder())
        if os.path.isfile(os.path.join(get_contents_folder(), file))
    ]
    if template_name not in templates_list:
        raise templates_exceptions.TemplateNotFound(template_name, language=language)

    return f"{template_name}.html"