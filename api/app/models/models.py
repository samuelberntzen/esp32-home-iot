from typing import Optional
from datetime import datetime
from sqlalchemy import Boolean, Column
from dataclasses import dataclass, field
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, FLOAT, INTEGER
from sqlalchemy.orm import registry

from app.database.db import Base

temperature_schemaname = "sensorReadings"

class TemperatureReadings(Base):
    __tablename__ = "temperatureReadings"


    id = Column(INTEGER, primary_key = True, index = False)
    dateTimeUtc = Column(TIMESTAMP, primary_key = False, index = True)
    temperatureCelsius = Column(FLOAT)
    humidityPercentage = Column(FLOAT)