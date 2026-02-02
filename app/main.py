from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="Collector V1",
    version="0.1.0",
    debug=settings.debug,
)


@app.get("/", tags=["root"])
def root() -> dict:
    return {
        "service": settings.app_name,
        "env": settings.environment,
        "message": "Collector V1 skeleton is running",
    }


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok"}



app.include_router(auth_router)
app.include_router(users_router)