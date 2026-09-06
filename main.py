from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import auth_router
from app.core.config import settings
from app.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application lifecycle, performing graceful resource cleanup on shutdown."""
    yield
    # Gracefully dispose database connection pools on shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# Register CORS middleware
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Register authentication routes under API prefix
app.include_router(auth_router, prefix=settings.API_PREFIX)


@app.get("/", summary="Root Welcome Endpoint")
async def root() -> dict[str, str]:
    return {"message": "Welcome to FastAPI Starter Kit"}


@app.get("/health", tags=["system"], summary="Service Health Check")
async def health_check() -> dict[str, str]:
    """Cloud-native liveness and readiness probe endpoint."""
    return {"status": "ok"}
