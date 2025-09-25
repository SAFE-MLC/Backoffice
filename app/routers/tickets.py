from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Ticket
from app.services.tickets import generar_session_token

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])

class TicketSessionRequest(BaseModel):
    ticketId: str

class TicketSessionResponse(BaseModel):
    ticketId: str
    sessionToken: str
    expiresAt: str

@router.post("/session", response_model=TicketSessionResponse)
def crear_ticket_session(req: TicketSessionRequest, db: Session = Depends(get_db)):
    if not req.ticketId:
        raise HTTPException(status_code=400, detail="ticketId requerido")

    ticket = db.query(Ticket).filter(Ticket.id == req.ticketId).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    if ticket.status != "ACTIVE":
        raise HTTPException(status_code=401, detail="Ticket no está activo")

    session_token, exp_time = generar_session_token(ticket.id)

    return {
        "ticketId": ticket.id,
        "sessionToken": session_token,
        "expiresAt": exp_time.isoformat().replace("+00:00", "Z"),
    }
