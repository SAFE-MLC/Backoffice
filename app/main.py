from fastapi import FastAPI
from app.routers import staff, tickets, warmup

app = FastAPI()

app.include_router(staff.router)
app.include_router(tickets.router)
app.include_router(warmup.router)