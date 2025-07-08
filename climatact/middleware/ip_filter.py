from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class IPFilterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_ips: list[str]):
        super().__init__(app)
        self.allowed_ips = allowed_ips
        self.excluded_paths = ["/docs", "/openapi.json", "/redoc"]

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        client_ip = request.client.host

        # Allow access to docs and schema always
        if any(path.startswith(excluded) for excluded in self.excluded_paths):
            return await call_next(request)
        
        if client_ip not in self.allowed_ips:
            return JSONResponse(
                status_code=403,
                content={
                    "details": "Forbidden: IP not allowed"
                }
            )
        response = await call_next(request)
        return response
