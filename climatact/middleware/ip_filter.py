import ipaddress
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class IPFilterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_ips: list[str]):
        super().__init__(app)
        self.allowed_ips = [ipaddress.ip_network(cidr) for cidr in allowed_ips]
        self.excluded_paths = ["/docs", "/openapi.json", "/redoc"]

    def ip_allowed(self, ip: str) -> bool:
        try:
            ip_addr = ipaddress.ip_address(ip)
            return any(ip_addr in net for net in self.allowed_ips)
        except ValueError:
            # Invalid IP format
            return False

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Allow access to docs and schema always
        if any(path.startswith(excluded) for excluded in self.excluded_paths):
            return await call_next(request)

        # Get client IP from X-Forwarded-For header if present (important if behind proxy)
        x_forwarded_for = request.headers.get("x-forwarded-for")
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.client.host

        if not self.ip_allowed(client_ip):
            return JSONResponse(
                status_code=403,
                content={
                    "detail": f"Forbidden: IP {client_ip} not allowed"
                }
            )
        response = await call_next(request)
        return response
