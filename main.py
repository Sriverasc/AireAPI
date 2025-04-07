from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database.config import get_db
from models.air_quality import AirQuality
from models.air_quality_inside import AirQualityInside
from schemas.air_quality import AirQualitySchema
from schemas.air_quality_inside import AirQualityInsideSchema
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from service import air_quality_service as aqs


# uvicorn api.main:app --reload
app = FastAPI()

@app.get("/air_quality/outside", response_model=list[AirQualitySchema])
def get_air_quality(db: Session = Depends(get_db), location = str):
    return aqs.get_data(AirQuality, AirQualitySchema, db)

@app.get("/air_quality/inside", response_model=list[AirQualityInsideSchema])
def get_air_quality_inside(db: Session = Depends(get_db), location = str):
    return aqs.get_data(AirQualityInside, AirQualityInsideSchema, db)

@app.get("/air_quality/outside/", response_model=list[AirQualitySchema])
def get_air_quality_by_date(
    start_date: str = Query(..., description="Fecha y hora de inicio de la consulta"),
    end_date: str = Query(..., description="Fecha y fin de fin de la consulta"),
    db: Session = Depends(get_db)
):
    datos = aqs.get_data_by_date(AirQuality, AirQualitySchema, db, start_date, end_date)
    return datos

@app.get("/air_quality/inside/", response_model=list[AirQualityInsideSchema])
def get_air_quality_inside_by_date(
    start_date: str = Query(..., description="Fecha y hora de inicio de la consulta"),
    end_date: str = Query(..., description="Fecha y fin de fin de la consulta"),
    db: Session = Depends(get_db)
):
    datos = aqs.get_data_by_date(AirQualityInside, AirQualityInsideSchema, db, start_date, end_date)
    return datos

@app.get("/air_quality/outside/periods", response_model=list[AirQualitySchema])
def get_air_quality_by_periods(
    start_date: str = Query(..., example="2025-02-10"),  
    end_date: str = Query(..., example="2025-02-15"),  
    start_hour: str = Query(..., example="05:30"), 
    end_hour: str = Query(..., example="07:45"),  
    db: Session = Depends(get_db)
):
    datos = aqs.get_data_by_periods(
        AirQuality, AirQualitySchema, db, start_date, end_date, start_hour, end_hour
    )

    return datos

@app.get("/air_quality/inside/periods", response_model=list[AirQualityInsideSchema])
def get_air_quality_by_periods(
    start_date: str = Query(..., example="2025-02-10"),  
    end_date: str = Query(..., example="2025-02-15"),  
    start_hour: str = Query(..., example="05:30"), 
    end_hour: str = Query(..., example="07:45"),  
    db: Session = Depends(get_db)
):
    datos = aqs.get_data_by_periods(
        AirQualityInside, AirQualityInsideSchema, db, start_date, end_date, start_hour, end_hour
    )

    return datos

@app.get("/air_quality/outside/periods/exact_hour", response_model=list[AirQualitySchema])
def get_air_quality_by_exact_hour(
    start_date: str = Query(..., example="2025-02-10"),  
    end_date: str = Query(..., example="2025-02-15"),  
    exact_hour: str = Query(..., example="05:30"),  # Ahora solo acepta HH:MM
    db: Session = Depends(get_db)
):
    data = aqs.get_data_by_exact_hour(
        AirQuality, AirQualitySchema, db, start_date, end_date, exact_hour
    )
    
    return data

@app.get("/air_quality/inside/periods/exact_hour", response_model=list[AirQualityInsideSchema])
def get_air_quality_by_exact_hour(
    start_date: str = Query(..., example="2025-02-10"),  
    end_date: str = Query(..., example="2025-02-15"),  
    exact_hour: str = Query(..., example="05:30"),  # Ahora solo acepta HH:MM
    db: Session = Depends(get_db)
):
    data = aqs.get_data_by_exact_hour(
        AirQualityInside, AirQualityInsideSchema, db, start_date, end_date, exact_hour
    )
    
    return data

@app.post("/air_quality/outside", response_model=AirQualitySchema)
def create_air_quality(
    data: AirQualitySchema,
    db: Session = Depends(get_db)
):
    return aqs.create_data(data, db, AirQuality)

@app.post("/air_quality/inside", response_model=AirQualityInsideSchema)
def create_air_quality_inside(
    data: AirQualityInsideSchema,
    db: Session = Depends(get_db)
):
    return aqs.create_data(data, db, AirQualityInside)

@app.put("/air_quality/outside/{date_time}", 
        response_model=AirQualitySchema
        )
def update_air_quality(
    date_time: datetime,
    data: AirQualitySchema,
    db: Session = Depends(get_db)
):
    return aqs.update_data(data, db, AirQuality, date_time)

@app.put("/air_quality/inside/{date_time}", 
        response_model=AirQualityInsideSchema
        )
def update_air_quality_inside(
    date_time: datetime,
    data: AirQualityInsideSchema,
    db: Session = Depends(get_db)
):
    return aqs.update_data(data, db, AirQualityInside, date_time)

@app.delete("/air_quality/outside/{date_time}")
def delete_air_quality(
    date_time: datetime,
    db: Session = Depends(get_db)
):
    return aqs.delete_data(date_time, db, AirQuality)

@app.delete("/air_quality/inside/{date_time}")
def delete_air_quality_inside(
    date_time: datetime,
    db: Session = Depends(get_db)
):
    return aqs.delete_data(date_time, db, AirQualityInside)