from pydantic import BaseModel
from typing import Optional

class StaffLoginRequest(BaseModel):
    staffId: str
    pin: str

class StaffLoginResponse(BaseModel):
    staffId: str
    displayName: str
    role: str
    gateId: Optional[str] = None
    zoneCheckpointId: Optional[str] = None
