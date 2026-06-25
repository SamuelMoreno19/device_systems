import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

# Cargamos las variables del archivo .env
load_dotenv()

# 1. Configuración del contexto de encriptación con Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Configuración de parámetros JWT obtieniendo valores seguros del .env
SECRET_KEY = os.getenv("SECRET_KEY", "llave_secreta_temporal_adso_sena_2026_super_segura")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def get_password_hash(password: str) -> str:
    """Toma la contraseña en texto plano y devuelve el hash seguro para guardar en la BD."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña que ingresa el usuario coincide con el hash guardado."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera un Token JWT firmado con un tiempo de expiración."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Añadimos la fecha de expiración al token
    to_encode.update({"exp": expire})
    
    # Firmamos el token con nuestra SECRET_KEY y el algoritmo HS256
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decodifica un token JWT y valida si es auténtico o si ya expiró."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None