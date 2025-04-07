from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mssql import DATETIME2

Base = declarative_base()

class AirQualityInside(Base):
    __tablename__ = "Calidad_Aire_Interior"

    date_time = Column(DATETIME2(7), primary_key=True, nullable=False)
    tvoc_mg_m3 = Column(Float)
    pm2_5_ug_m3 = Column(Integer)
    co2_ppm = Column(Float)
    temperature_c = Column(Float)
    humidity_rh = Column(Float)

    def to_string(self):
        return f"{self.date_time}, {self.tvoc_mg_m3}, {self.pm2_5_ug_m3}, {self.co2_ppm}, {self.temperature_c}, {self.humidity_rh}"