from config import settings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from backend.src.users import router as user_router
from backend.src.auth import router as auth_router

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

app.include_router(auth_router.router)
app.include_router(user_router.router)

@app.get("/", response_class=RedirectResponse)
def home():
    return RedirectResponse(settings.website_url)