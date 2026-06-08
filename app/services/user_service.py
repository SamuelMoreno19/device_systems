from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user_model import Usuario
from app.schemas.user_schema import UserCreate, UserUpdatePartial
from fastapi import HTTPException, status

class UserService:
    
    @staticmethod
    def listar_usuarios(db: Session, role: Optional[str] = None, is_active: Optional[bool] = None) -> List[Usuario]:
        # 1. Preparamos la consulta base (Es como un SELECT * FROM usuarios)
        query = db.query(Usuario)
        
        # 2. Si mandan filtro de rol, lo aplicamos en el WHERE
        if role is not None:
            query = query.filter(Usuario.role == role.lower())
            
        # 3. Si mandan filtro de estado activo, lo aplicamos en el WHERE
        if is_active is not None:
            query = query.filter(Usuario.is_active == is_active)
            
        # 4. Ejecutamos la consulta y retornamos la lista de registros
        return query.all()

    @staticmethod
    def crear_usuario(db: Session, user_in: UserCreate) -> Usuario:
        # Creamos la instancia del modelo con los datos validados de Pydantic
        nuevo_usuario = Usuario(**user_in.model_dump())
        
        db.add(nuevo_usuario)      # 1. Lo agregamos a la sesión
        db.commit()                # 2. Guardamos los cambios físicamente en el test.db
        db.refresh(nuevo_usuario)  # 3. Refrescamos para que nos devuelva el ID autogenerado
        return nuevo_usuario

    @staticmethod
    def actualizar_completo(db: Session, usuario_db: Usuario, datos_nuevos: UserCreate) -> Usuario:
        # Reemplazo completo campo por campo usando PUT
        usuario_db.name = datos_nuevos.name
        usuario_db.email = datos_nuevos.email
        usuario_db.role = datos_nuevos.role
        usuario_db.is_active = datos_nuevos.is_active
        
        db.commit()
        db.refresh(usuario_db)
        return usuario_db

    @staticmethod
    def actualizar_parcial(db: Session, usuario_db: Usuario, datos_nuevos: UserUpdatePartial) -> Usuario:
        # Convertimos a diccionario excluyendo lo que venga vacío (None)
        campos_enviados = datos_nuevos.model_dump(exclude_unset=True)
        
        if not campos_enviados:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Intento de actualización sin datos. Debe enviar al menos un campo."
            )
            
        # Recorremos solo los campos enviados y los actualizamos en el objeto de la DB
        for llave, valor in campos_enviados.items():
            setattr(usuario_db, llave, valor)
            
        db.commit()
        db.refresh(usuario_db)
        return usuario_db

    @staticmethod
    def eliminar_usuario(db: Session, usuario_db: Usuario):
        db.delete(usuario_db) # Le decimos a la DB que borre el registro
        db.commit()           # Confirmamos la eliminación permanente