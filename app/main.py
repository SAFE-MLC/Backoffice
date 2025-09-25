from fastapi import FastAPI
from app.routers import staff, tickets

app = FastAPI()

app.include_router(staff.router)
app.include_router(tickets.router)