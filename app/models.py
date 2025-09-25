from sqlalchemy import Column, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_at = Column(DateTime(timezone=True), nullable=False)
    end_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False, default="SCHEDULED")

    gates = relationship("Gate", back_populates="event")
    zones = relationship("Zone", back_populates="event")
    tickets = relationship("Ticket", back_populates="event")

class Gate(Base):
    __tablename__ = "gates"

    id = Column(String, primary_key=True, index=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    name = Column(String, nullable=False)

    event = relationship("Event", back_populates="gates")
    staff = relationship("Staff", back_populates="gate")

class Zone(Base):
    __tablename__ = "zones"

    id = Column(String, primary_key=True, index=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    name = Column(String, nullable=False)

    event = relationship("Event", back_populates="zones")
    checkpoints = relationship("ZoneCheckpoint", back_populates="zone")

class ZoneCheckpoint(Base):
    __tablename__ = "zone_checkpoints"

    id = Column(String, primary_key=True, index=True)
    zone_id = Column(String, ForeignKey("zones.id"), nullable=False)
    name = Column(String, nullable=False)

    zone = relationship("Zone", back_populates="checkpoints")
    staff = relationship("Staff", back_populates="zone_checkpoint")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, index=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    holder = Column(String)
    status = Column(String, nullable=False)  # ACTIVE | USED | REVOKED
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    used_at = Column(DateTime(timezone=True))

    event = relationship("Event", back_populates="tickets")
    entitlements = relationship("ZoneEntitlement", back_populates="ticket")
    scans = relationship("TicketScan", back_populates="ticket")

class ZoneEntitlement(Base):
    __tablename__ = "zone_entitlements"

    ticket_id = Column(String, ForeignKey("tickets.id"), primary_key=True)
    zone_id = Column(String, ForeignKey("zones.id"), primary_key=True)

    ticket = relationship("Ticket", back_populates="entitlements")
    zone = relationship("Zone")

class Staff(Base):
    __tablename__ = "staff"

    id = Column(String, primary_key=True, index=True)
    display_name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # GATE | ZONE
    pin_hash = Column(String, nullable=False)

    gate_id = Column(String, ForeignKey("gates.id"))
    zone_checkpoint_id = Column(String, ForeignKey("zone_checkpoints.id"))

    gate = relationship("Gate", back_populates="staff")
    zone_checkpoint = relationship("ZoneCheckpoint", back_populates="staff")

class TicketScan(Base):
    __tablename__ = "ticket_scans"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ticket_id = Column(String, ForeignKey("tickets.id"), nullable=False)
    kind = Column(String, nullable=False)  # GATE | ZONE
    gate_id = Column(String, ForeignKey("gates.id"))
    zone_checkpoint_id = Column(String, ForeignKey("zone_checkpoints.id"))
    ts = Column(DateTime(timezone=True), server_default=func.now())

    ticket = relationship("Ticket", back_populates="scans")

class ZonePresence(Base):
    __tablename__ = "zone_presence"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ticket_id = Column(String, ForeignKey("tickets.id"), nullable=False)
    zone_id = Column(String, ForeignKey("zones.id"), nullable=False)
    checkpoint_id = Column(String, ForeignKey("zone_checkpoints.id"), nullable=False)
    direction = Column(String, nullable=False)  # IN
    ts = Column(DateTime(timezone=True), server_default=func.now())

