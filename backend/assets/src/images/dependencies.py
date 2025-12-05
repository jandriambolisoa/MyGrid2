import os

from backend.assets.dependencies import valid_file_name_uniqueness, valid_filename


def get_images_folder():
    folderpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage")
    if not os.path.isdir(folderpath):
        os.mkdir(folderpath)
    return folderpath.replace("\\", "/")

async def valid_image_name_uniqueness(image_name, language: str = "en"):
    valid_name = await valid_file_name_uniqueness(image_name, get_images_folder(), language)

    return valid_name

async def valid_image_filename(filename, language: str = "en"):
    valid_name = await valid_filename(filename, get_images_folder(), language)

    return valid_name
