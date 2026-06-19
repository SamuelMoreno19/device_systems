from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db  # Revisa que este import coincida con tu proyecto
from app.schemas.device_schema import DeviceCreate, DeviceResponse
from app.services.device_service import DeviceService

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED, summary="Registrar un nuevo dispositivo")
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    return DeviceService.create_device(db=db, device_data=device)

@router.get("/", response_model=List[DeviceResponse], summary="Obtener lista de todos los dispositivos")
def get_all_devices(db: Session = Depends(get_db)):
    return DeviceService.get_all_devices(db=db)

@router.get("/{device_id}", response_model=DeviceResponse, summary="Obtener detalles de un dispositivo por ID")
def get_device_by_id(device_id: int, db: Session = Depends(get_db)):
    return DeviceService.get_device_by_id(db=db, device_id=device_id)