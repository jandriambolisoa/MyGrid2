import os

from backend.assets import exceptions as assets_exceptions

async def valid_file_name_uniqueness(name: str, folder: str, language: str = "en"):
    files = [
        os.path.splitext(file)[0]
        for file in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, file))
    ]
    if name in files:
        raise assets_exceptions.AssetFileAlreadyExistsException(language=language)

    return name

async def valid_filename(filename: str, folder:str, language: str = "en"):
    files = [
        file
        for file in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, file))
    ]
    if filename not in files:
        raise assets_exceptions.FileNotFoundException(language=language)

    return filename
