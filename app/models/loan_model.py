from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.connection import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    loan_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    return_date = Column(DateTime, nullable=True)
    status = Column(String, default="active", nullable=False) # active, returned, overdue

    # Relaciones Fase 6: Cada préstamo pertenece a un usuario (Usuario) y a un dispositivo (Device)
    user = relationship("Usuario", back_populates="loans")
    device = relationship("Device", back_populates="loans")