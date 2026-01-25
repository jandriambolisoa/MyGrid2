from backend.mailings.config import settings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from backend.mailings.src.templates import router as templates_router
from backend.mailings.src.writing import router as writing_router
from backend.mailings.src.sending import router as sending_router

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

app.include_router(templates_router.router)
app.include_router(writing_router.router)
app.include_router(sending_router.router)