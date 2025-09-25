from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Ticket
from config import SESSION_KEY

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])

class TicketSessionRequest(BaseModel):
    ticketId: str

class TicketSessionResponse(BaseModel):
    ticketId: str
    sessionKey: str

@router.post("/session", response_model=TicketSessionResponse)
def crear_ticket_session(req: TicketSessionRequest, db: Session = Depends(get_db)):
    if not req.ticketId:
        raise HTTPException(status_code=400, detail="ticketId requerido")

    ticket = db.query(Ticket).filter(Ticket.id == req.ticketId).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    if ticket.status != "ACTIVE":
        raise HTTPException(status_code=401, detail="Ticket no está activo")

    return {
        "ticketId": ticket.id,
        "sessionKey": SESSION_KEY,
    }
