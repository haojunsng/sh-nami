from fastapi import FastAPI
from climatact.middleware.ip_filter import IPFilterMiddleware
from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from climatact.settings.constants import ALLOWED_IPS

def setup_middlewares(app: FastAPI):

    app.add_middleware(IPFilterMiddleware, allowed_ips=ALLOWED_IPS)

    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
