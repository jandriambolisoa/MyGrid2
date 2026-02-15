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
    prefix="/collectibles",
    tags= ["collectibles"]
)

#
# CRUD operations
#

@router.get("/{name}/model", response_class=FileResponse, status_code=status.HTTP_200_OK)
async def get_collectible_model(name: str, owner_id: int = None, db: Database = Depends(get_db), current_user: UserSelf = Depends(get_current_user)):
    if owner_id and owner_id != current_user.id:
        db.cursor.execute("""\
            UPDATE userscollectibles
            SET views = userscollectibles.views + 1
            FROM collectibles
            WHERE userscollectibles.collectible_id = collectibles.id 
            AND userscollectibles.user_id = %s
            AND collectibles.name = %s""", (owner_id, name))
        db.conn.commit()

    response = requests.get(f"{app_settings.ms_assets_url}/glb/{name}.glb",stream=True)
    return StreamingResponse(response.iter_content(chunk_size=CHUNK_SIZE), response.status_code, headers={
        "Content-Type": response.headers.get("Content-Type", "model/gltf-binary"),
        "Content-Disposition": response.headers.get("Content-Disposition", f"attachment; filename={name}.glb")
    })

@router.get("/{name}/textures", response_class=FileResponse, status_code=status.HTTP_200_OK)
async def get_collectible_textures(name: str, current_user: UserSelf = Depends(get_current_user)):
    response = requests.get(f"{app_settings.ms_assets_url}/images/{name}.jpg",stream=True)
    return StreamingResponse(response.iter_content(chunk_size=CHUNK_SIZE), response.status_code, headers={
        "Content-Type": response.headers.get("Content-Type", "image/jpeg"),
        "Content-Disposition": response.headers.get("Content-Disposition", f"inline; filename={name}.jpg")
    })

@router.get("/{name}/icon", response_class=FileResponse, status_code=status.HTTP_200_OK)
async def get_collectible_icon(name: str, current_user: UserSelf = Depends(get_current_user)):
    response = requests.get(f"{app_settings.ms_assets_url}/images/icon_{name}.png",stream=True)
    return StreamingResponse(response.iter_content(chunk_size=CHUNK_SIZE), response.status_code, headers={
        "Content-Type": response.headers.get("Content-Type", "image/png"),
        "Content-Disposition": response.headers.get("Content-Disposition", f"inline; filename=icon_{name}.png")
    })
