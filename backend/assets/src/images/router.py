import os

from fastapi import APIRouter, Depends, status, UploadFile
from fastapi.responses import FileResponse

from PIL import Image

from backend.assets.src.images import exceptions as images_exceptions
from backend.assets.src.images.dependencies import valid_image_name_uniqueness, get_images_folder, valid_image_filename
from backend.assets.src.images.constants import IMAGE_MAX_SIZE
from backend.assets.constants import SEARCH_LIMIT

router = APIRouter(
    prefix="/images",
    tags= ["images"]
)


@router.post("/{image_name}", status_code=status.HTTP_201_CREATED)
async def upload_image(file: UploadFile, image_name: str = Depends(valid_image_name_uniqueness), max_size: int = IMAGE_MAX_SIZE, extension: str = ".jpg", language ="en"):
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

    return f"{image_name}{extension}"

@router.get("/search", response_model=list[str])
async def search_images(limit: int = SEARCH_LIMIT, page: int = 0, language = "en"):
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


@router.delete("/{filename}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(filename: str = Depends(valid_image_filename), language: str = "en"):
    filepath = os.path.join(get_images_folder(), filename)
    os.remove(filepath)