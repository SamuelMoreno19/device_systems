from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user_model import Usuario  # Usamos 'Usuario' que es como se llama tu modelo
from app.auth.security import decode_access_token

# Define que el endpoint para loguearse y obtener el token estará en /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    """
    Extrae el token de la cabecera, lo decodifica y busca al usuario en la base de datos.
    Si el token no es válido o expiró, corta la petición con un error 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales de acceso.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decodificamos el token usando la lógica de security.py
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # Extraemos el username (guardado tradicionalmente bajo el claim 'sub')
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
        
    # Buscamos al usuario en SQLite
    user = db.query(Usuario).filter(Usuario.name == username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Valida si el usuario autenticado está activo."""
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo.")
    return current_user

class RoleChecker:
    """
    Clase verificadora para bloquear endpoints según el rol del usuario (Fase 8).
    Permite crear filtros rápidos como 'solo admin' o 'admin y support'.
    """
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: Usuario = Depends(get_current_active_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permisos insuficientes para ejecutar esta operación."
            )
        return current_user

# Instancias listas para proteger tus rutas más adelante:
require_admin_or_support = RoleChecker(["admin", "support"])
require_admin = RoleChecker(["admin"])