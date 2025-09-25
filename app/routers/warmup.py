# app/routers/warmup.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db, redis_client

router = APIRouter(prefix="/internal", tags=["internal"])

@router.post("/warmup")
def warmup(eventId: str, db: Session = Depends(get_db)):
    """
    Hidrata Redis con tickets y checkpoints para un evento.
    """
    try:
        # ------------------------
        # Tickets + entitlements
        # ------------------------
        tickets_query = text("""
            SELECT t.id, t.status,
                   COALESCE(array_agg(ze.zone_id) FILTER (WHERE ze.zone_id IS NOT NULL), '{}') AS entitlements
            FROM tickets t
            LEFT JOIN zone_entitlements ze ON ze.ticket_id = t.id
            WHERE t.event_id = :event_id
            GROUP BY t.id
        """)
        rows = db.execute(tickets_query, {"event_id": eventId}).mappings().all()

        for row in rows:
            ticket_data = {
                "status": row["status"],
                "entitlements": row["entitlements"],
                "eventId": eventId
            }
            redis_client.set(f"ticket:{row['id']}", str(ticket_data), ex=3600) 

        # ------------------------
        # Checkpoints
        # ------------------------
        checkpoints_query = text("""
            SELECT zc.id, z.id as zone_id, z.name as zone_name
            FROM zone_checkpoints zc
            JOIN zones z ON zc.zone_id = z.id
            WHERE z.event_id = :event_id
        """)
        zc_rows = db.execute(checkpoints_query, {"event_id": eventId}).mappings().all()

        for zc in zc_rows:
            checkpoint_data = {
                "zoneId": zc["zone_id"],
                "zoneName": zc["zone_name"],
                "eventId": eventId
            }
            redis_client.set(f"checkpoint:{zc['id']}", str(checkpoint_data), ex=3600)

        return {"status": "ok", "eventId": eventId}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
