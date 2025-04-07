from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mssql import DATETIME2

Base = declarative_base()

class AirQuality(Base):
    __tablename__ = "Calidad_Aire_Exterior"
    
    date_time = Column(DATETIME2(7), primary_key=True, nullable=False)
    aqi = Column(Integer, nullable=True)
    aqi_alto = Column(Integer, nullable=True)
    pm1_ug_m3 = Column(Integer, nullable=True)
    pm1_alto_ug_m3 = Column(Integer, nullable=True)
    pm25_ug_m3 = Column(Integer, nullable=True)
    pm25_alto_ug_m3 = Column(Integer, nullable=True)
    pm10_ug_m3 = Column(Integer, nullable=True)
    pm10_alto_ug_m3 = Column(Integer, nullable=True)
    temp_c = Column(Integer, nullable=True)
    temp_max_c = Column(Integer, nullable=True)
    temp_min_c = Column(Integer, nullable=True)
    humedad_pct = Column(Integer, nullable=True)
    humedad_max_pct = Column(Integer, nullable=True)
    humedad_min_pct = Column(Integer, nullable=True)
    punto_rocio_c = Column(Integer, nullable=True)
    punto_rocio_max_c = Column(Integer, nullable=True)
    punto_rocio_min_c = Column(Integer, nullable=True)
    bulbo_humedo_c = Column(Integer, nullable=True)
    bulbo_humedo_max_c = Column(Integer, nullable=True)
    bulbo_humedo_min_c = Column(Integer, nullable=True)
    indice_calor_c = Column(Integer, nullable=True)
    indice_calor_max_c = Column(Integer, nullable=True)

    def to_string(self):
        return f"{self.date_time}: AQI={self.aqi}, PM1={self.pm1_ug_m3}, PM2.5={self.pm25_ug_m3}, PM10={self.pm10_ug_m3}, Temp={self.temp_c}, Hum={self.humedad_pct}, Punto de rocío={self.punto_rocio_c}, Bulbo húmedo={self.bulbo_humedo_c}, Índice de calor={self.indice_calor_c}"
