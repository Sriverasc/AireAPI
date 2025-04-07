from pydantic import BaseModel, Field, field_validator
from datetime import datetime, UTC

class AirQualityInsideSchema(BaseModel):
    date_time: datetime = Field(..., example="2025-03-11T19:55:00", description="Fecha y hora en formato ISO 8601")
    tvoc_mg_m3: float
    pm2_5_ug_m3: int
    co2_ppm: float
    temperature_c: float
    humidity_rh: float

    @field_validator("date_time")
    def validate_date(cls, value):
        if not isinstance(value, datetime):
            raise ValueError("Formato de fecha inválido. Debe ser un datetime válido en ISO 8601.")

        # Convertir `value` a UTC si no tiene zona horaria
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)  # Agrega UTC

        # Validar que la fecha no sea futura
        if value > datetime.now(UTC):
            raise ValueError("La fecha no puede ser en el futuro.")

        return value  # Retorna la fecha válida
    
    class Config:
        from_attributes = True  # Permite convertir desde SQLAlchemy
        extra = "forbid"