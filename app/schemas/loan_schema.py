from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.device_schema import DeviceResponse

# Ojo: Importa aquí el schema de respuesta de tu Usuario actual. 
# Si en tu archivo de usuarios se llama 'UserResponse' o 'UsuarioResponse', cámbialo aquí:
from app.schemas.user_schema import UserResponse 

# Lo que se pide para registrar un préstamo
class LoanCreate(BaseModel):
    user_id: int
    device_id: int

# Lo que responde la API de forma básica
class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True

# FASE 11: Schema avanzado con la información anidada (JOIN)
class LoanDetailResponse(LoanResponse):
    user: UserResponse
    device: DeviceResponse

    class Config:
        from_attributes = True