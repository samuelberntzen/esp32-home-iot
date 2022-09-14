from sqlalchemy.orm import Session
from app.models import schemas, models 
from app.database import db


def get_temperature_readings_all(db: Session): # Add to_time for filtering 

    data = db.query(models.TemperatureReadings).all()

    return data 

def get_temperature_readings_latest(db: Session): # Add to_time for filtering 

    data = db.query(models.TemperatureReadings).order_by(models.TemperatureReadings.dateTimeUtc.desc()).first()

    return data

def get_temperature_readings_date(db: Session, item: schemas.TemperatureReadingsDate):

    data = db.query(models.TemperatureReadings).filter(
        models.TemperatureReadings.dateTimeUtc >= item.start_date).filter(
            models.TemperatureReadings.dateTimeUtc <= item.end_date
        ).all()

    return data 

def insert_temperature_readings(db: Session, item: schemas.TemperatureReadingsCreate):

    db_item = models.TemperatureReadings(
        dateTimeUtc = item.dateTimeUtc,
        temperatureCelsius = item.temperatureCelcius,
        humidityPercentage = item.humidityPercentage
    )

    # Insert to database
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

def delete_temperature_reading_from_date(db: Session, item: schemas.TemperatureReadingsDelete):

    db.query(models.TemperatureReadings).filter(
        models.TemperatureReadings.dateTimeUtc >= item.start_date).filter(
            models.TemperatureReadings.dateTimeUtc <= item.end_date
        ).delete()

    db.commit()
     

