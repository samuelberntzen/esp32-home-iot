from pydantic import BaseModel
import datetime 

class TemperatureReadings(BaseModel):
    utcTime: str
    temperatureCelcius: float
    humidityPercentage: float

class fireSensorReadings(BaseModel):
    utcTime: str
    isFire: int