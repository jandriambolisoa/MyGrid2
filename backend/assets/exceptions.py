from fastapi import HTTPException, status

from jinja2 import Environment

from backend.assets.texts import *


class AssetFileAlreadyExistsException(HTTPException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = asset_file_already_exists_message[language]

class FileNotFoundException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = file_not_found_message[language]
