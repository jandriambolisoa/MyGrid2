import requests
from fastapi import APIRouter, Depends, status
from starlette.responses import FileResponse, RedirectResponse, StreamingResponse

from backend.config import settings as app_settings
from backend.db.database import get_db, Database
from backend.oauth2 import get_current_user
from backend.src.collectibles.constants import CHUNK_SIZE
from backend.src.users.exceptions import NotAUserError
from backend.src.users.schemas import UserSelf

router = APIRouter(
    prefix="/images",
    tags= ["images"]
)

#
# CRUD operations
#

@router.get("/{image_name}", response_class=FileResponse, status_code=status.HTTP_200_OK)
async def get_user_image(image_name: str):
    response = requests.get(f"{app_settings.ms_assets_url}/images/{image_name}.jpg",stream=True)
    return StreamingResponse(response.iter_content(chunk_size=CHUNK_SIZE), response.status_code, headers={
        "Content-Type": response.headers.get("Content-Type", "image/jpeg"),
        "Content-Disposition": response.headers.get("Content-Disposition", f"inline; filename={image_name}.jpg")
    })
