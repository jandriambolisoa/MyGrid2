import os

from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse

from jinja2 import Environment
from jinja2 import FileSystemLoader

from backend.mailings.src.templates.contents import get_contents_folder
from backend.mailings.src.templates.dependencies import valid_template_name
from backend.mailings.src.writing import exceptions as writing_exceptions

router = APIRouter(
    prefix="/writing",
    tags= ["writing"]
)

@router.get("/{template_name}/fields", status_code=status.HTTP_200_OK)
async def read_template_fields(template_name: str = Depends(valid_template_name), language: str = "en"):
    with open(os.path.join(get_contents_folder(), template_name), "r", encoding="utf-8") as f:
        content = f.read()

    fields = list(set([v.split("}}")[0].strip() for v in content.split("{{")[1:]]))

    if not fields:
        raise writing_exceptions.NoFieldsFound(language=language)

    return fields


@router.post("/{template_name}", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def write_email(fields: dict, template_name: str = Depends(valid_template_name), language: str = "en"):
    environment = Environment(loader=FileSystemLoader(get_contents_folder()))
    template = environment.get_template(f"{template_name}")
    if sorted(list(fields.keys())) != sorted(await read_template_fields(template_name = template_name, language = language)):
        raise writing_exceptions.InvalidFieldsException(language=language)

    return template.render(**fields)
