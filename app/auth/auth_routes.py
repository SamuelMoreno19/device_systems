from fastapi import APIRouter, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.auth_schema import UserRegister, UserResponse, Token
from app.auth.auth_service import AuthService 
from app.dependencies.auth_dependency import get_current_active_user
from app.models.user_model import Usuario
from app.middlewares.request_middleware import limiter

# Creamos el enrutador
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")  # Limitador Fase 11
def register(request: Request, user_in: UserRegister, db: Session = Depends(get_db)):
    """Registra nuevos usuarios delegando la validación y creación al servicio."""
    return AuthService.register_user(db, user_in)


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")  # Limitador Fase 11
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Inicia sesión y genera el token JWT delegando el proceso al servicio."""
    return AuthService.login_user(db, form_data)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: Usuario = Depends(get_current_active_user)):
    """Ruta protegida (Fase 8) que retorna el perfil del usuario autenticado actual."""
    return current_user