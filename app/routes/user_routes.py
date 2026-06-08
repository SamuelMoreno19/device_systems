from fastapi import APIRouter, Depends, Response, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdatePartial
from app.services.user_service import UserService
from app.dependencies.database_dependency import get_user_or_404, verificar_correo_duplicado, get_db

router = APIRouter(prefix="/users", tags=["Users"])

# Tu función original de firmas con los headers personalizados
def agregar_firmas_ocultas(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"

# GET: Listar todo y filtrar en la DB
@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK, summary="Listar y filtrar usuarios desde la DB")
def obtener_usuarios(
    response: Response,
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db) # <--- Inyectamos la sesión de la base de datos
):
    agregar_firmas_ocultas(response)
    return UserService.listar_usuarios(db, role, is_active)

# GET: Buscar por ID (Usa la inyección get_user_or_404 que ya busca en la DB)
@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Buscar usuario por ID en la DB")
def buscar_por_id(response: Response, usuario: dict = Depends(get_user_or_404)):
    agregar_firmas_ocultas(response)
    return usuario

# POST: Registrar Usuario en la DB real
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Registrar un nuevo usuario en la DB")
def crear_usuario(user_in: UserCreate, response: Response, db: Session = Depends(get_db)):
    agregar_firmas_ocultas(response)
    verificar_correo_duplicado(user_in.email, db)
    return UserService.crear_usuario(db, user_in)

# PUT: Actualización completa en la DB
@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Actualización completa de un usuario")
def actualizar_usuario_completo(
    user_in: UserCreate, 
    response: Response, 
    usuario: dict = Depends(get_user_or_404),
    db: Session = Depends(get_db)
):
    agregar_firmas_ocultas(response)
    verificar_correo_duplicado(user_in.email, db, excluir_id=usuario.id)
    return UserService.actualizar_completo(db, usuario, user_in)

# PATCH: Actualización parcial en la DB
@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Actualización parcial de un usuario")
def actualizar_usuario_parcial(
    user_in: UserUpdatePartial, 
    response: Response, 
    usuario: dict = Depends(get_user_or_404),
    db: Session = Depends(get_db)
):
    agregar_firmas_ocultas(response)
    if user_in.email:
        verificar_correo_duplicado(user_in.email, db, excluir_id=usuario.id)
    return UserService.actualizar_parcial(db, usuario, user_in)

# DELETE: Eliminar usuario de la DB permanente
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un usuario del sistema")
def eliminar_usuario(response: Response, usuario: dict = Depends(get_user_or_404), db: Session = Depends(get_db)):
    agregar_firmas_ocultas(response)
    UserService.eliminar_usuario(db, usuario)
    return Response(status_code=status.HTTP_204_NO_CONTENT)