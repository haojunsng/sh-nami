import os
from fastapi import FastAPI, HTTPException, Security, Depends, Request
from fastapi.security.api_key import APIKeyHeader
from climatact.services.weather_service import get_weather_metrics
from climatact.models.models import WeatherResponse
from climatact.middleware.setup import setup_middlewares

API_KEY = os.environ.get("API_KEY")
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def create_app() -> FastAPI:
    app = FastAPI()

    setup_middlewares(app)

    async def get_api_key(api_key: str = Security(api_key_header)):
        if api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid or missing API Key")

    @app.get("/weather", response_model=WeatherResponse, dependencies=[Depends(get_api_key)])
    @app.state.limiter.limit("10/minute")
    async def get_weather(town: str, request: Request):
        response = await get_weather_metrics(town)
        return response

    return app

app = create_app()
