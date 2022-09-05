from fastapi import APIRouter
from fastapi import Query
from typing import Optional
from app.models.models import TemperatureReadings
import datetime

router = APIRouter(
    prefix="/temperature",
    tags=["temperature"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_root() -> dict:
    """Test endpoint for checking connection

    Returns:
        dict: connection successfull
    """
    return {"connection": "successfull"}

@router.post("/readings/", response_model = TemperatureReadings)
async def load_readings(readings_payload: TemperatureReadings):
    """Loads payload data into the database, returns the payload for verification

    Returns:
        dict: Original payload for verification purposes
    """

    print(f"Received body was: \n \t {readings_payload}")

    return readings_payload 

