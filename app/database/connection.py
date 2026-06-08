from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 1. Dirección de nuestra base de datos local (creará un archivo llamado test.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# 2. Crear el motor de conexión (El puente físico)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} # Obligatorio para que FastAPI use varios hilos con SQLite
)

# 3. La fábrica de sesiones (El molde para abrir conexiones limpias)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# 4. La clase Padre de la que heredarán nuestros futuros modelos
class Base(DeclarativeBase):
    pass

# Importamos el modelo para que la clase Base registre los metadatos de la tabla antes de crearla
from app.models.user_model import Usuario

# 5. Función para que FastAPI cree las tablas automáticamente al encender
def create_tables():
    Base.metadata.create_all(bind=engine)