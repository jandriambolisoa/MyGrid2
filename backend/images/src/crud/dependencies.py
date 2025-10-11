import os

from backend.images.src.crud import exceptions as images_exceptions

def get_images_folder():
    folderpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage")
    if not os.path.isdir(folderpath):
        os.mkdir(folderpath)
    return folderpath.replace("\\", "/")

async def valid_image_uniqueness(image_name, language: str = "en"):
    images_list = [
        os.path.splitext(file)[0]
        for file in os.listdir(get_images_folder())
        if os.path.isfile(os.path.join(get_images_folder(), file))
    ]
    if image_name in images_list:
        raise images_exceptions.ImageAlreadyExistsException(language=language)

    return image_name

async def valid_image_name(image_name, language: str = "en"):
    images_list = [
        os.path.splitext(file)[0]
        for file in os.listdir(get_images_folder())
        if os.path.isfile(os.path.join(get_images_folder(), file))
    ]
    if image_name not in images_list:
        raise images_exceptions.ImageNotFoundException(language=language)

    return image_name

async def valid_filename(filename, language: str = "en"):
    files_list = [
        file
        for file in os.listdir(get_images_folder())
        if os.path.isfile(os.path.join(get_images_folder(), file))
    ]
    if filename not in files_list:
        raise images_exceptions.ImageNotFoundException(language=language)

    return filename