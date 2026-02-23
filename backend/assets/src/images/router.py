import os

from fastapi import APIRouter, Depends, status, UploadFile
from fastapi.responses import FileResponse

from PIL import Image

from backend.assets.schemas import RenameAsset
from backend.assets.src.images import exceptions as images_exceptions
from backend.assets.src.images.dependencies import valid_image_name_uniqueness, get_images_folder, valid_image_filename
from backend.assets.src.images.constants import IMAGE_MAX_SIZE
from backend.assets.constants import SEARCH_LIMIT

router = APIRouter(
    prefix="/images",
    tags= ["images"]
)


@router.post("/{image_name}", status_code=status.HTTP_201_CREATED)
async def upload_image(file: UploadFile, image_name: str = Depends(valid_image_name_uniqueness), max_size: int = IMAGE_MAX_SIZE, extension: str = ".jpg", language: str ="en"):
    # Format extension in the right way
    extension = extension if extension.startswith(".") else "." + extension

    file_content = file.file.read() # bytes
    filepath = os.path.join(get_images_folder(), f"{image_name}{extension}")

    # Store image
    writer = open(filepath, "wb")
    writer.write(file_content)
    writer.close()

    # Compress image
    image = Image.open(filepath)
    width, height = image.size
    if width > max_size or height > max_size:
        if width > max_size:
            ratio = max_size / width
        else:
            ratio = max_size / height

        image = image.resize((round(width*ratio), round(height*ratio)), Image.Resampling.BICUBIC)
        image.save(filepath, quality=66)

    return filepath

@router.get("/search", response_model=list[str])
async def search_images(limit: int = SEARCH_LIMIT, page: int = 0, language: str = "en"):
    offset = limit * page

    images_files = [
        file
        for file in os.listdir(get_images_folder())
    ]

    if not images_files:
        raise images_exceptions.ImageNotFoundException(language=language)

    return images_files[offset:offset+limit]


@router.get("/{filename}", status_code=status.HTTP_200_OK, response_class=FileResponse)
async def read_image(filename: str = Depends(valid_image_filename), language: str = "en"):
    filepath = os.path.join(get_images_folder(), filename)
    return FileResponse(filepath)

@router.put("/rename", status_code=status.HTTP_200_OK)
async def rename_glb(datas: RenameAsset, language: str = "en", extension: str = ".jpg"):
    old_name = datas.old_name if datas.old_name.endswith(f".{extension}") == -1 else f"{datas.old_name}.{extension}"
    new_name = datas.new_name if datas.new_name.endswith(f".{extension}") == -1 else f"{datas.new_name}.{extension}"

    old_filepath = os.path.join(get_images_folder(), old_name)
    new_filepath = os.path.join(get_images_folder(), new_name)
    if not os.path.isfile(old_filepath):
        raise images_exceptions.ImageNotFoundException(language=language)

    os.renames(old_filepath, new_filepath)

    return new_filepath

@router.delete("/{filename}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(filename: str = Depends(valid_image_filename), language: str = "en"):
    filepath = os.path.join(get_images_folder(), filename)
    os.remove(filepath)