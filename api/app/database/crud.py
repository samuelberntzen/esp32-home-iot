from sqlalchemy.orm import Session
from api.app.models.models import TemperatureReadings
from app.models import models, schemas


def get_temperature_readings(db: Session, from_time: str): # Add to_time for filtering 
     return db.query(models.TemperatureReadings).all()

def insert_temperature_readings(db: Session, schema: schemas.TemperatureReadings):
    temperature_readings = models.TemperatureReadings(
        dateTimeUTC=schemas.utcTime, 
        temperatureCelsius = schemas.temperatureCelsius, 
        humidityPercentage = schemas.humidityPercentage
        )

    # Insert to database
    db.add(temperature_readings)
    db.commit()
    db.refresh(temperature_readings)


