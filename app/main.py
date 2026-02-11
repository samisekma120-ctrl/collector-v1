import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.categories import router as categories_router
from app.api.routes.users import router as users_router
from app.core.config import settings
from app.core.logging import setup_logging

# Initialise le logging AVANT de créer l'app
setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Collector V1",
    version="0.1.0",
    debug=settings.debug,
)

# -------------------------------------------------------------------
# CORS (front de démonstration uniquement – V1)
# -------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # React (Vite)
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        # Front statique éventuel
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        # si tu ouvres un fichier en file:// (évite en démo si possible)
        "null",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["root"])
def root() -> dict:
    logger.info(
        "root endpoint called",
        extra={"service": settings.app_name, "env": settings.environment},
    )
    return {
        "service": settings.app_name,
        "env": settings.environment,
        "message": "Collector V1 skeleton is running",
    }

@app.get("/health", tags=["health"])
def health() -> dict:
    logger.debug("health check called")
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(categories_router)
