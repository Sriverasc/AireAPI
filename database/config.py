from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configurar url:
SERVER = 'CONEJITO12V2\\SQLEXPRESS'  # Ejemplo: 'localhost\SQLEXPRESS' o '192.168.1.100'
DB = 'Aire'

# Configurar la cadena de conexión
DATABASE_URL = f'mssql+pyodbc://{SERVER}/{DB}?trusted_connection=yes&driver=SQL+Server'

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para obtener la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

