from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(prefix="/api/v1")


@router.get("/app")
async def app_info():
    return {
        "name": settings.APP_NAME,
        "env": settings.APP_ENV,
        "version": "1.0.0",
    }
