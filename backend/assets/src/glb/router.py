import os

from fastapi import APIRouter, Depends, status, UploadFile
from fastapi.responses import FileResponse

from backend.assets.constants import SEARCH_LIMIT
from backend.assets.src.glb.dependencies import valid_glb_name_uniqueness, valid_glb_filename, get_glb_folder
from backend.assets.src.glb import exceptions as glb_exceptions

router = APIRouter(
    prefix="/glb",
    tags= ["glb"]
)


@router.post("/{glb_name}", status_code=status.HTTP_201_CREATED)
async def upload_glb(file: UploadFile, glb_name: str = Depends(valid_glb_name_uniqueness), language ="en"):
    file_content = file.file.read() # bytes
    filepath = os.path.join(get_glb_folder(), f"{glb_name}.glb")

    # Store image
    writer = open(filepath, "wb")
    writer.write(file_content)
    writer.close()

    return f"{glb_name}.glb"


@router.get("/search", response_model=list[str])
async def search_glb(limit: int = SEARCH_LIMIT, page: int = 0, language = "en"):
    offset = limit * page

    files = [
        file
        for file in os.listdir(get_glb_folder())
    ]

    if not files:
        raise glb_exceptions.GLBFileNotFoundException(language=language)

    return files[offset:offset+limit]


@router.get("/{filename}", status_code=status.HTTP_200_OK, response_class=FileResponse)
async def read_glb(filename: str = Depends(valid_glb_filename), language: str = "en"):
    filepath = os.path.join(get_glb_folder(), filename)
    return FileResponse(filepath)


@router.delete("/{filename}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_glb(filename: str = Depends(valid_glb_filename), language: str = "en"):
    filepath = os.path.join(get_glb_folder(), filename)
    os.remove(filepath)
