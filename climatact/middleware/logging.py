import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable

logger = logging.getLogger("climatact")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(handler)

logger.propagate = False


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        logger.info(f"Request: {request.method} {request.url.path}")
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(f"Exception during handling {request.method} {request.url.path}: {e}")
            raise
        logger.info(f"Response: {response.status_code} for {request.method} {request.url.path}")
        return response
