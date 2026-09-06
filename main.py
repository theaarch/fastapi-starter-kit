from fastapi import FastAPI

from app.api.auth import auth_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
)

# Register authentication routes under API prefix
app.include_router(auth_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Starter Kit"}
