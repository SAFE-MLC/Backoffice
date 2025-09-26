import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("backoffice")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = (time.perf_counter() - start_time) * 1000  # ms

        logger.info(
            f"{request.method} {request.url.path} "
            f"status={response.status_code} "
            f"duration={process_time:.2f}ms"
        )
        return response
