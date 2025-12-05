from fastapi import HTTPException, status

from jinja2 import Environment

from backend.assets.src.glb.texts import *


class GLBFileNotFoundException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = glb_file_not_found_message[language]
