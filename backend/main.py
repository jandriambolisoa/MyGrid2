from starlette import status
from starlette.responses import Response

from backend.config import settings

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# from backend.src.appstatus import router as user_router
from backend.src.auth import router as auth_router
from backend.src.collectibles import router as collectibles_router
from backend.src.auth.apple import validate_apple_token
from backend.src.drivers import router as drivers_router
from backend.src.events import router as events_router
from backend.src.images import router as images_router
from backend.src.live import router as live_router
from backend.src.nav import router as nav_router
from backend.src.predictions import router as predictions_router
from backend.src.ranks import router as ranks_router
from backend.src.registrations import router as registrations_router
from backend.src.results import router as results_router
from backend.src.scores import router as scores_router
from backend.src.users import router as users_router

from backend.src.collectibles import listener as collectibles_listener
from backend.src.live import listener as live_listener
from backend.src.auth import listener as auth_listener
from backend.src.predictions import listener as predictions_listener
from backend.src.ranks import listener as ranks_listener
from backend.src.results import listener as results_listener
from backend.src.scores import listener as scores_listener

from backend.scheduler import scheduler

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

collectibles_listener.init_listener()
auth_listener.init_listener()
live_listener.init_listener()
predictions_listener.init_listener()
ranks_listener.init_listener()
results_listener.init_listener()
scores_listener.init_listener()

app.include_router(auth_router.router)
app.include_router(collectibles_router.router)
app.include_router(drivers_router.router)
app.include_router(events_router.router)
app.include_router(images_router.router)
app.include_router(live_router.router)
app.include_router(nav_router.router)
app.include_router(predictions_router.router)
app.include_router(ranks_router.router)
app.include_router(results_router.router)
app.include_router(scores_router.router)
app.include_router(registrations_router.router)
app.include_router(users_router.router)

scheduler.start()

@app.get("/", response_class=RedirectResponse)
def home():
    return RedirectResponse(settings.website_url)
