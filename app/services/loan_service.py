from sqlalchemy.orm import Session
from app.models.loan_model import Loan
from app.models.device_model import Device
from app.models.user_model import Usuario # Tu clase en español
from app.schemas.loan_schema import LoanCreate
from fastapi import HTTPException, status
from datetime import datetime, timezone

class LoanService:
    @staticmethod
    def create_loan(db: Session, loan_data: LoanCreate):
        # 1. Validar que el usuario exista
        user = db.query(Usuario).filter(Usuario.id == loan_data.user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")

        # 2. Validar que el dispositivo exista
        device = db.query(Device).filter(Device.id == loan_data.device_id).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo no encontrado.")

        # 3. REGLA DE ORO: Validar si el dispositivo está disponible
        if not device.is_available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El dispositivo ya se encuentra prestado actualmente."
            )

        # 4. Registrar el préstamo
        new_loan = Loan(
            user_id=loan_data.user_id,
            device_id=loan_data.device_id,
            status="active"
        )
        
        # 5. Cambiar el estado del dispositivo a NO disponible
        device.is_available = False

        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)
        return new_loan

    @staticmethod
    def return_device(db: Session, loan_id: int):
        # 1. Buscar el préstamo activo
        loan = db.query(Loan).filter(Loan.id == loan_id, Loan.status == "active").first()
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No se encontró un préstamo activo con ese ID."
            )

        # 2. Marcar devolución en el préstamo
        loan.return_date = datetime.now(timezone.utc)
        loan.status = "returned"

        # 3. Volver a poner el dispositivo disponible
        device = db.query(Device).filter(Device.id == loan.device_id).first()
        if device:
            device.is_available = True

        db.commit()
        db.refresh(loan)
        return loan

    @staticmethod
    def get_loans_with_join(db: Session, username: str = None, status_filter: str = None):
        # FASE 11: Consulta avanzada usando .join() para cargar las relaciones
        query = db.query(Loan).join(Loan.user).join(Loan.device)

        # Filtros opcionales
        if username:
            query = query.filter(Usuario.name.ilike(f"%{username}%"))
        if status_filter:
            query = query.filter(Loan.status == status_filter)

        return query.all()