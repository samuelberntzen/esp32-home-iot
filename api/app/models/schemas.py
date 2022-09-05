# TODO: Add schema for temperature table 

from typing import Optional
from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float

# from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.database.db import Base

temperature_schemaname = "temperature"

class TemperatureReadings(Base):

    __table_args__ = {"schema": temperature_schemaname}
    __tablename__ = "temperatureReadings"

    dateTimeUTC = Column(String, primary_key=True, index=True)
    temperatureCelsius = Column(float, unique=False, index=False)
    humidityPercentage = Column(float, unique=False, index=False)
