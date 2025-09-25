from app.database import SessionLocal, engine
from app.models import Base, Event, Gate, Zone, ZoneCheckpoint, Staff, Ticket, ZoneEntitlement
from datetime import datetime, timedelta

db = SessionLocal()

event = Event(
    id="evt_1",
    name="Concierto",
    start_at=datetime.utcnow() + timedelta(hours=1),
    end_at=datetime.utcnow() + timedelta(hours=5),
    status="SCHEDULED"
)
db.add(event)

gate = Gate(id="gate_1", event_id="evt_1", name="Puerta Norte")
db.add(gate)

zone = Zone(id="zone_vip", event_id="evt_1", name="VIP")
db.add(zone)

checkpoint = ZoneCheckpoint(id="zc_10", zone_id="zone_vip", name="Entrada VIP A")
db.add(checkpoint)

staff1 = Staff(id="carlos", display_name="Carlos", role="GATE", pin_hash="1234", gate_id="gate_1")
staff2 = Staff(id="maya", display_name="Maya", role="ZONE", pin_hash="4321", zone_checkpoint_id="zc_10")
db.add_all([staff1, staff2])

ticket1 = Ticket(id="t1", event_id="evt_1", holder="Alice", status="ACTIVE")
ticket2 = Ticket(id="t2", event_id="evt_1", holder="Bob", status="ACTIVE")
db.add_all([ticket1, ticket2])

entitlement = ZoneEntitlement(ticket_id="t1", zone_id="zone_vip")
db.add(entitlement)

db.commit()
db.close()

print("Database seeded successfully!")
