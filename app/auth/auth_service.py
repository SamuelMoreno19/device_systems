from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user_model import Usuario
from app.schemas.auth_schema import UserRegister
from app.auth.security import get_password_hash, verify_password, create_access_token

class AuthService:
    @staticmethod
    def register_user(db: Session, user_in: UserRegister):
        # 1. Validar duplicados
        if db.query(Usuario).filter(Usuario.email == user_in.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado."
            )
        if db.query(Usuario).filter(Usuario.name == user_in.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya se encuentra registrado."
            )
        
        # 2. Encriptar y guardar
        hashed_pwd = get_password_hash(user_in.password)
        new_user = Usuario(
            name=user_in.username,
            email=user_in.email,
            hashed_password=hashed_pwd,
            role=user_in.role,
            is_active=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def login_user(db: Session, form_data: OAuth2PasswordRequestForm):
        # 1. Verificar credenciales
        user = db.query(Usuario).filter(Usuario.name == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales de acceso incorrectas.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 2. Generar token
        access_token = create_access_token(data={"sub": user.name, "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}