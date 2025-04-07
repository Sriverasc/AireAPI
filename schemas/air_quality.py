from pydantic import BaseModel, Field, field_validator
from datetime import datetime, UTC

class AirQualitySchema(BaseModel):
    date_time: datetime = Field(..., example="2025-03-11T19:55:00", description="Fecha y hora en formato ISO 8601")
    aqi: int
    aqi_alto: int
    pm1_ug_m3: int
    pm1_alto_ug_m3: int
    pm25_ug_m3: int
    pm25_alto_ug_m3: int
    pm10_ug_m3: int
    pm10_alto_ug_m3: int
    temp_c: int
    temp_max_c: int
    temp_min_c: int
    humedad_pct: int
    humedad_max_pct: int
    humedad_min_pct: int
    punto_rocio_c: int
    punto_rocio_max_c: int
    punto_rocio_min_c: int
    bulbo_humedo_c: int
    bulbo_humedo_max_c: int
    bulbo_humedo_min_c: int
    indice_calor_c: int
    indice_calor_max_c: int

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
