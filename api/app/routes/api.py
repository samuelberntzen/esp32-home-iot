from fastapi import APIRouter
from app.endpoints import temperature

router = APIRouter()
router.include_router(temperature.router)
