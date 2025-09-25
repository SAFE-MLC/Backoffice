from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db   

router = APIRouter(prefix="/api/staff", tags=["staff"])

@router.post("/login", response_model=schemas.StaffLoginResponse)
def staff_login(payload: schemas.StaffLoginRequest, db: Session = Depends(get_db)):
    staff = db.query(models.Staff).filter(models.Staff.id == payload.staffId).first()
    if not staff:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if staff.pin_hash != payload.pin:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return schemas.StaffLoginResponse(
        staffId=staff.id,
        displayName=staff.display_name,
        role=staff.role,
        gateId=staff.gate_id,
        zoneCheckpointId=staff.zone_checkpoint_id,
    )
