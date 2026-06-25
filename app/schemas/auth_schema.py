import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

class UserRegister(BaseModel):
    # Usamos Field de Pydantic v2 para limitar la longitud del nombre de usuario
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")
    email: EmailStr = Field(..., description="Email válido obligatorio")
    password: str = Field(..., description="Contraseña que debe cumplir con las políticas de seguridad")
    role: str = Field(default="user", description="Roles válidos: admin, support, user")

    # 1. Validador estricto para los roles permitidos
    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        allowed_roles = ["admin", "support", "user"]
        if value.lower() not in allowed_roles:
            raise ValueError("El rol especificado no es permitido. Use: admin, support o user.")
        return value.lower()

    # 2. Validador avanzado para la fuerza de la contraseña (Fase 6)
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("La contraseña debe tener mínimo 8 caracteres.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe incluir al menos una letra mayúscula.")
        if not re.search(r"[a-z]", value):
            raise ValueError("La contraseña debe incluir al menos una letra minúscula.")
        if not re.search(r"[0-9]", value):
            raise ValueError("La contraseña debe incluir al menos un número.")
        if " " in value:
            raise ValueError("La contraseña no debe contener espacios en blanco.")
        return value

class UserLogin(BaseModel):
    username: str = Field(..., description="Nombre de usuario para iniciar sesión")
    password: str = Field(..., description="Contraseña en texto plano")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    # Configuración de Pydantic v2 para leer los modelos de SQLAlchemy (reemplaza al viejo orm_mode)
    model_config = ConfigDict(from_attributes=True)