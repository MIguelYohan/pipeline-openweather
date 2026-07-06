from db import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

class Climate(Base):
    __tablename__ = "climate"

    id = Column(Integer, primary_key= True, autoincrement= True)
    local = Column(String(50), nullable= False)
    temperature = Column(Float, nullable= False)
    temp_min = Column(Float)
    temp_max = Column(Float)
    feels_like = Column(Float)
    description = Column(String(50))
    condition = Column(String(20))
    clouds = Column(Integer)
    wind_speed = Column(Float)
    wind_direction = Column(Integer)
    wind_gust_speed = Column(Float)
    collect_time = Column(DateTime, nullable= False, default=datetime.now)

    def __init__(
            self, local, temperature, temp_min, temp_max, feels_like, description,
            condition, clouds, wind_speed, wind_direction, wind_gust_speed
            ):
        self.local = local
        self.temperature = temperature
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.feels_like = feels_like
        self.description = description
        self.condition = condition
        self.clouds = clouds
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.wind_gust_speed = wind_gust_speed
        