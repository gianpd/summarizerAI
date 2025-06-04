from fastapi import APIRouter, Depends

from app.config import Settings, get_settings

router = APIRouter()

@router.get("/")
async def home(setting: Settings = Depends(get_settings)):
    return {"Home": "text summaries home"}

@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
