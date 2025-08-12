from fastapi import HTTPException, status

from backend.src.appstatus.texts import maintenance_message

class MaintenanceServerError(HTTPException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    def __init__(self, language: str, **kwargs):
        super().__init__(**kwargs)
        self.detail = maintenance_message[language]
