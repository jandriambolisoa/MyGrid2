import os

from backend.assets.dependencies import valid_file_name_uniqueness, valid_filename


def get_glb_folder():
    folderpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage")
    if not os.path.isdir(folderpath):
        os.mkdir(folderpath)
    return folderpath.replace("\\", "/")

async def valid_glb_name_uniqueness(name, language: str = "en"):
    await valid_file_name_uniqueness(name, get_glb_folder(), language)

    return name

async def valid_glb_filename(filename, language: str = "en"):
    valid_name = await valid_filename(filename, get_glb_folder(), language)

    return valid_name
