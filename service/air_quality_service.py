from typing import Type, List, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, and_, extract
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from schemas.air_quality import AirQualitySchema
from models.air_quality import AirQuality

T = TypeVar("T", bound=BaseModel)  # `T` será un tipo basado en Pydantic

def get_data(
    model: Type,  
    schema: Type[T],  
    db: Session
) -> List[T]:
    return db.query(model).all()

def get_data_by_date(
    model: Type,  
    schema: Type[T],  
    db: Session,
    start_date: str,  
    end_date: str
) -> List[T]:
    try:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")

        if start_date_dt > end_date_dt:
            raise HTTPException(status_code=400, detail="La fecha de inicio debe ser menor o igual que la fecha de fin.")

        # Consultar base de datos
        datos = db.query(model).filter(
            model.date_time >= start_date_dt,
            model.date_time <= end_date_dt
        ).all()

        return datos

    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al consultar datos: {}".format(str(e)))

def get_data_by_periods(
    model: Type,  
    schema: Type[T],  
    db: Session,
    start_date: str,  
    end_date: str,  
    start_hour: str, 
    end_hour: str,  
) -> List[T]:
    try:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha incorrecto o fecha invalida. Use YYYY-MM-DD con dias y meses habiles.")

    if start_date_dt > end_date_dt:
        raise HTTPException(status_code=400, detail="La fecha de inicio debe ser menor o igual que la fecha de fin.")

    try:
        start_hour, start_minute = map(int, start_hour.split(":"))
        end_hour, end_minute = map(int, end_hour.split(":"))

        if not (0 <= start_hour < 24 and 0 <= start_minute < 60):
            raise ValueError
        if not (0 <= end_hour < 24 and 0 <= end_minute < 60):
            raise ValueError

    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de hora incorrecto. Use HH:MM con valores válidos.")

    if (start_hour, start_minute) >= (end_hour, end_minute) and start_date_dt == end_date_dt:
        raise HTTPException(status_code=400, detail="La hora de inicio debe ser menor que la hora de fin en el mismo día.")

    stmt = select(model).where(
        and_(
            model.date_time >= start_date_dt,
            model.date_time <= end_date_dt,
            and_(
                extract("hour", model.date_time) * 60 + extract("minute", model.date_time)
                >= start_hour * 60 + start_minute,
                extract("hour", model.date_time) * 60 + extract("minute", model.date_time)
                <= end_hour * 60 + end_minute,
            )
        )
    )

    resultados = db.execute(stmt).scalars().all()
    
    return resultados

def get_data_by_exact_hour(
    model: Type,  
    schema: Type[T],  
    db: Session,
    start_date: str,
    end_date: str,
    exact_hour: str
) -> List[T]:
    try:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha incorrecto o fecha invalida. Use YYYY-MM-DD con dias y meses habiles.")

    if start_date_dt > end_date_dt:
        raise HTTPException(status_code=400, detail="La fecha de inicio debe ser menor o igual que la fecha de fin.")

    try:
        hour, minute = map(int, exact_hour.split(":"))
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de hora incorrecto. Use HH:MM con valores válidos.")

    stmt = select(model).where(
        and_(
            model.date_time >= start_date_dt,
            model.date_time < end_date_dt + timedelta(days=1),
            extract("hour", model.date_time) == hour,
            extract("minute", model.date_time) == minute,
        )
    )

    resultados = db.execute(stmt).scalars().all()
    
    return resultados

def create_data(
    data: Type[T],
    db: Session,
    model: Type[T]
):
    try:
        # Verificar si ya existe un registro con la misma fecha
        existing_record = db.query(model).filter(model.date_time == data.date_time).first()
        if existing_record:
            raise HTTPException(status_code=400, detail="Ya existe un registro con esta fecha.")

        # Crear el objeto utilizando el modelo proporcionado (AirQuality o AirQualityInterior)
        air_quality = model(**data.model_dump())  # Usamos el modelo adecuado dependiendo del tipo de datos

        db.add(air_quality)  # Agregar el objeto a la sesión de la base de datos
        db.commit()  # Guardar los cambios
        db.refresh(air_quality)  # Refrescar el objeto para obtener los datos actualizados

        return air_quality  # Devolver el objeto recién creado

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error de integridad al guardar datos.")
    except Exception as e:
        db.rollback()  # En caso de error, revertir los cambios
        raise HTTPException(status_code=500, detail=f"Error al guardar datos: {str(e)}")

def update_data(
    data: Type[T],
    db: Session,
    model: Type[T],
    date_time: datetime
):
    try:
        # date_time a string
        date_time_str = date_time.strftime("%Y-%m-%d %H:%M:%S")

        # Validar fecha y hora válida
        datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

        # Consultar objeto utilizando filtro para 'date_time'
        air_quality = db.query(model).filter(model.date_time == date_time).first()

        if air_quality is None:
            raise HTTPException(status_code=404, detail="Datos no encontrados.")

        # Actualizar objeto
        for key, value in data.model_dump().items():
            setattr(air_quality, key, value)

        db.commit()
        db.refresh(air_quality)  # Refrescar para obtener datos actualizados

        return air_quality  # Devolver el objeto actualizado

    except HTTPException as e:
        # Re-lanzar la excepción HTTP sin modificarla
        raise e

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar datos: {str(e)}")

def delete_data(
    date_time: datetime,
    db: Session,
    model: Type[T]
):
    try:
        # Consultar objeto
        air_quality = db.query(model).get(date_time)

        if air_quality is None:
            raise HTTPException(status_code=404, detail="Datos no encontrados.")

        db.delete(air_quality)
        db.commit()

        return {"message": "Datos eliminados."}

    except HTTPException as e:
        # Re-lanzar la excepción HTTP sin modificarla
        raise e

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar los datos: {str(e)}")