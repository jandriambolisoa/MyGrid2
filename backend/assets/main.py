from backend.assets.config import settings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.assets.src.images import router as images_router
from backend.assets.src.glb import router as glb_router

docs_urls = {
    "docs_url": "/docs" if settings.debug else None,
    "redoc_url": "/redoc" if settings.debug else None,
    "openapi_url": "/openapi.json" if settings.debug else None,
}
app = FastAPI(**docs_urls)

# Init middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(images_router.router)
app.include_router(glb_router.router)