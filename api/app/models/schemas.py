from pydantic import BaseModel
import datetime 

class TemperatureReadingsBase(BaseModel):
    class Config:
        orm_mode = True

class TemperatureReadingsCreate(TemperatureReadingsBase):
    dateTimeUtc: str
    temperatureCelcius: float
    humidityPercentage: float

class TemperatureReadingsGet(TemperatureReadingsCreate):
    id: int

class TemperatureReadingsDelete(TemperatureReadingsBase):
    start_date: str
    end_date: str

class TemperatureReadingsDate(TemperatureReadingsDelete):
    pass 

class fireSensorReadings(BaseModel):
    dateTimeUtc: str
    isFire: int