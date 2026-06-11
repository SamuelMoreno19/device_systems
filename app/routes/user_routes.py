from fastapi import APIRouter, Depends, Response, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdatePartial
from app.services.user_service import UserService
from app.dependencies.database_dependency import get_user_or_404, verificar_correo_duplicado, get_db
from app.models.user_model import Usuario

router = APIRouter(prefix="/users", tags=["Users"])

def agregar_firmas_ocultas(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"

# GET: Listar, filtrar y ORDENAR en la DB (Fase 8 y 9)
@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK, summary="Listar, filtrar y ordenar usuarios desde la DB")
def obtener_usuarios(
    response: Response,
    role: Optional[str] = Query(None, description="Filtrar por rol: admin, support, user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    order_by: Optional[str] = Query("name", description="Ordenar por: 'name' o 'created_at'"), # ⚠️ NUEVO: Parámetro para cumplir la Fase 8
    db: Session = Depends(get_db)
):
    agregar_firmas_ocultas(response)
    return UserService.listar_usuarios(db, role, is_active, order_by)

# GET: Buscar por ID
@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Buscar usuario por ID en la DB")
def buscar_por_id(response: Response, usuario: Usuario = Depends(get_user_or_404)):
    agregar_firmas_ocultas(response)
    return usuario

# POST: Registrar Usuario
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Registrar un nuevo usuario en la DB")
def crear_usuario(user_in: UserCreate, response: Response, db: Session = Depends(get_db)):
    agregar_firmas_ocultas(response)
    verificar_correo_duplicado(user_in.email, db)
    return UserService.crear_usuario(db, user_in)

# PUT: Actualización completa
@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Actualización completa de un usuario")
def actualizar_usuario_completo(
    user_in: UserCreate, 
    response: Response, 
    usuario: Usuario = Depends(get_user_or_404),
    db: Session = Depends(get_db)
):
    agregar_firmas_ocultas(response)
    verificar_correo_duplicado(user_in.email, db, excluir_id=usuario.id)
    return UserService.actualizar_completo(db, usuario, user_in)

# PATCH: Actualización parcial
@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Actualización parcial de un usuario")
def actualizar_usuario_parcial(
    user_in: UserUpdatePartial, 
    response: Response, 
    usuario: Usuario = Depends(get_user_or_404),
    db: Session = Depends(get_db)
):
    agregar_firmas_ocultas(response)
    if user_in.email:
        verificar_correo_duplicado(user_in.email, db, excluir_id=usuario.id)
    return UserService.actualizar_parcial(db, usuario, user_in)

# DELETE: Eliminar usuario de la DB permanente
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un usuario del sistema")
def eliminar_usuario(response: Response, usuario: Usuario = Depends(get_user_or_404), db: Session = Depends(get_db)):
    agregar_firmas_ocultas(response)
    UserService.eliminar_usuario(db, usuario)
    return Response(status_code=status.HTTP_204_NO_CONTENT)