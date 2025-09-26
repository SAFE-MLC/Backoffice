import logging
import time
import json
from fastapi import FastAPI, Request

from app.routers import staff, tickets, warmup

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "service": "backoffice",
            "message": record.getMessage(),
        }
        return json.dumps(log)

handler = logging.StreamHandler()  # stdout
handler.setFormatter(JsonFormatter())

logger = logging.getLogger("backoffice")
logger.setLevel(logging.INFO)
logger.handlers = [handler]
logger.propagate = False

app = FastAPI(title="Backoffice")

app.include_router(staff.router)
app.include_router(tickets.router)
app.include_router(warmup.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
    finally:
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} "
            f"({process_time:.2f} ms) from {request.client.host}"
        )
    return response

@app.on_event("startup")
async def startup_event():
    logger.info("Backoffice iniciado y listo para recibir requests")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Backoffice detenido")
