import os

from .contents import get_contents_folder
from .exceptions import TemplateNotFound

async def valid_template_name(template_name, language: str = "en"):
    templates_list = [os.path.splitext(file)[0] for file in os.listdir(get_contents_folder()) if os.path.isfile(file)]
    if template_name not in templates_list:
        raise TemplateNotFound(template_name, language=language)

    return template_name