from sqlalchemy.orm import Session
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate
from fastapi import HTTPException, status

class DeviceService:
    @staticmethod
    def create_device(db: Session, device_data: DeviceCreate):
        # Validar si el número de serie ya está registrado
        db_device = db.query(Device).filter(Device.serial_number == device_data.serial_number).first()
        if db_device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El número de serie ya está registrado en el sistema."
            )
        
        new_device = Device(
            name=device_data.name,
            serial_number=device_data.serial_number,
            device_type=device_data.device_type,
            brand=device_data.brand
        )
        db.add(new_device)
        db.commit()
        db.refresh(new_device)
        return new_device

    @staticmethod
    def get_all_devices(db: Session):
        return db.query(Device).all()

    @staticmethod
    def get_device_by_id(db: Session, device_id: int):
        device = db.query(Device).filter(Device.id == device_id).first()
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dispositivo no encontrado."
            )
        return device