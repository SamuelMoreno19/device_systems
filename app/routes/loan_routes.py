from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.connection import get_db
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services.loan_service import LoanService

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED, summary="Registrar el préstamo de un dispositivo")
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    return LoanService.create_loan(db=db, loan_data=loan)

@router.post("/{loan_id}/return", response_model=LoanResponse, summary="Registrar la devolución de un dispositivo")
def return_device(loan_id: int, db: Session = Depends(get_db)):
    return LoanService.return_device(db=db, loan_id=loan_id)

@router.get("/", response_model=List[LoanDetailResponse], summary="Consultar historial de préstamos con filtros")
def get_loans(
    username: Optional[str] = Query(None, description="Filtrar por nombre de usuario"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filtrar por estado (active, returned)"),
    db: Session = Depends(get_db)
):
    return LoanService.get_loans_with_join(db=db, username=username, status_filter=status_filter)