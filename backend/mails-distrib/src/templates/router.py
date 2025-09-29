import os

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import HTMLResponse

from .constants import SEARCH_LIMIT
from .contents import get_contents_folder, check_html_content
from .dependencies import valid_template_name
from .exceptions import NoTemplateFound, TemplateAlreadyExistsException
from .schemas import Content

router = APIRouter(
    prefix="/templates",
    tags= ["templates"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_template(content: Content, language = "en"):
    if content.filename in [file for file in os.listdir(get_contents_folder()) if os.path.isfile(file)]:
        raise TemplateAlreadyExistsException(language=language)
    check_html_content(content.content, language=language)

    return content

@router.get("/read", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def read_template(template_name: str = Depends(valid_template_name), language: str = "en"):
    with open(os.path.join(get_contents_folder(), template_name), "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content, status_code=status.HTTP_200_OK)

@router.get("/search", response_model=list[Content])
async def search_templates(limit: int = SEARCH_LIMIT, page: int = 0, language = "en"):
    offset = limit * page

    template_files = [file for file in os.listdir(get_contents_folder()) if os.path.isfile(file)]
    templates = []

    if not template_files:
        raise NoTemplateFound(language=language)

    for template in template_files[offset:offset + limit]:
        with open(os.path.join(get_contents_folder(), template)) as file:
            templates.append(Content(
                filename= os.path.splitext(template)[0],
                html= file.read()
            ))

    return templates
