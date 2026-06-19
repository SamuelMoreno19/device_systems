from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Lo que se pide para crear o actualizar un equipo
class DeviceBase(BaseModel):
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str] = None

class DeviceCreate(DeviceBase):
    pass  # Hereda todo lo de Base

# Lo que la API responde al consultar un equipo
class DeviceResponse(DeviceBase):
    id: int
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True