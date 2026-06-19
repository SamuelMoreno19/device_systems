from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base

# Creamos la clase Usuario que hereda de Base (la mamá de los modelos)
class Usuario(Base):
    # 1. Le decimos a SQLAlchemy cómo se va a llamar la tabla en la base de datos
    __tablename__ = "usuarios"

    # 2. Definimos las columnas de la tabla con sus tipos de datos reales
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relación Fase 6: Un usuario puede tener muchos préstamos [cite: 131, 132]
    # (Corregida la indentación exacta a 4 espacios para eliminar el error de Pylance)
    loans = relationship("Loan", back_populates="user")