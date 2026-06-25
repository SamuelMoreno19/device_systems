from fastapi import APIRouter, Depends, Query, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.middlewares.request_middleware import limiter
from app.database.connection import get_db
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services.loan_service import LoanService
from app.dependencies.auth_dependency import get_current_active_user, require_admin_or_support

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED, summary="Registrar el préstamo de un dispositivo")
@limiter.limit("10/minute")
def create_loan(
    request: Request,
    loan: LoanCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return LoanService.create_loan(db=db, loan_data=loan)

@router.post("/{loan_id}/return", response_model=LoanResponse, summary="Registrar la devolución de un dispositivo")
def return_device(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin_or_support)
):
    return LoanService.return_device(db=db, loan_id=loan_id)

@router.get("/", response_model=List[LoanDetailResponse], summary="Consultar historial de préstamos con filtros")
@limiter.limit("30/minute")
def get_loans(
    request: Request,
    username: Optional[str] = Query(None, description="Filtrar por nombre de usuario"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filtrar por estado (active, returned)"),
    db: Session = Depends(get_db),
    current_user = Depends(require_admin_or_support)
):
    return LoanService.get_loans_with_join(db=db, username=username, status_filter=status_filter)