import os

from fastapi import APIRouter, Depends, status, UploadFile
from fastapi.responses import HTMLResponse

from backend.mailings.src.templates.constants import SEARCH_LIMIT
from backend.mailings.src.templates.contents import get_contents_folder, check_html_content
from backend.mailings.src.templates.dependencies import valid_template_name
from backend.mailings.src.templates import exceptions as templates_exceptions
from backend.mailings.src.templates.schemas import Content

router = APIRouter(
    prefix="/templates",
    tags= ["templates"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_template(file: UploadFile, language = "en"):
    file_content = file.file.read().decode("utf-8")
    check_html_content(file_content, language=language)
    filepath = os.path.join(get_contents_folder(), file.filename)
    with open(filepath, "w") as f:
        f.write(file_content)

@router.get("/read", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def read_template(template_name: str = Depends(valid_template_name), language: str = "en"):
    with open(os.path.join(get_contents_folder(), template_name), "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content, status_code=status.HTTP_200_OK)

@router.get("/search", response_model=list[Content])
async def search_templates(limit: int = SEARCH_LIMIT, page: int = 0, language = "en"):
    offset = limit * page

    template_files = [
        file
        for file in os.listdir(get_contents_folder())
        if valid_template_name(file, language=language)
    ]
    templates = []

    if not template_files:
        raise templates_exceptions.NoTemplateFound(language=language)

    for template in template_files[offset:offset + limit]:
        with open(os.path.join(get_contents_folder(), template)) as file:
            templates.append(Content(
                filename= os.path.splitext(template)[0],
                html= file.read()
            ))

    return templates
