from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.models import models, schemas 
from app.database import crud
from app.database import db 
import datetime
from app.config import settings 

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

@router.get("/read/all/", response_model = list)
async def get_readings_all(db = Depends(db.get_db)):
    """_placeholder_

    Args:
        response_payload (schemas.TemperatureReadingsGet): _description_
    """

    data = crud.get_temperature_readings_all(db = db)

    return data

@router.get("/read/latest/")
async def get_readings_latest(db = Depends(db.get_db)):
    """_placeholder_

    Args:
        response_payload (schemas.TemperatureReadingsGet): _description_
    """

    data = crud.get_temperature_readings_latest(db = db)

    return data

@router.get("/read/date/")
async def get_readings_date(item: schemas.TemperatureReadingsDate, db = Depends(db.get_db)):
    """_placeholder_

    Args:
        response_payload (schemas.TemperatureReadingsGet): _description_
    """

    data = crud.get_temperature_readings_date(item = item, db = db)

    return data

@router.post("/add/")
async def add_readings(item: schemas.TemperatureReadingsCreate, db = Depends(db.get_db)):
    """Loads payload data into the database, returns the payload for verification

    Returns:
        dict: Original payload for verification purposes
    """

    crud.insert_temperature_readings(db = db, item = item)

    return item 

@router.post("/delete/date", response_model = dict)
async def delete_readings_from_date(date_payload: schemas.TemperatureReadingsDelete, db = Depends(db.get_db)):
    """Deletes rows from TemperatureReadings table between two specific dates

    Args:
        date_payload (schemas.TemperatureReadingsDelete): JSON payload containing start_date and end_date, e.g. "1999-01-01" og "1999-01-01 05:45:01"
        db (_type_, optional): DB session. Defaults to Depends(db.get_db).

    Returns:
        _type_: Message confirming successfull deletion of data
    """

    print(date_payload)

    crud.delete_temperature_reading_from_date(db = db, item = date_payload)

    return {
        "message": f"Successfully deleted object between {date_payload.start_date} and {date_payload.end_date} from database"
    }