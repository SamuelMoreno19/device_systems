from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal # Importamos la fábrica local
from app.models.user_model import Usuario

# 1. Función generadora de sesiones con ciclo de vida controlado
def get_db():
    db = SessionLocal() # Abre la puerta a la base de datos
    try:
        yield db # Te presta la sesión para que la uses en tu endpoint
    finally:
        db.close() # Pase lo que pase, cuando la petición termine, cierra la puerta

# 2. Dependencia para buscar un usuario por ID en la DB real o disparar 404 de una
def get_user_or_404(user_id: int, db: Session = Depends(get_db)) -> Usuario:
    # Hace un SELECT * FROM usuarios WHERE id = user_id LIMIT 1
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="El usuario que buscas no existe."
        )
    return usuario

# 3. Dependencia para verificar si un correo ya está en uso por otro usuario
def verificar_correo_duplicado(email: str, db: Session, excluir_id: int = None):
    query = db.query(Usuario).filter(Usuario.email == email)
    
    # Si estamos editando (PUT/PATCH), le decimos que ignore el ID del mismo usuario que se está editando
    if excluir_id is not None:
        query = query.filter(Usuario.id != excluir_id)
        
    usuario_existente = query.first()
    
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Ese correo ya existe, intenta con otro."
        )