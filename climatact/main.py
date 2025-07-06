from fastapi import FastAPI
from services.weather_service import get_weather_metrics
from models.models import WeatherResponse

app = FastAPI()


@app.get("/weather", response_model=WeatherResponse)
async def get_weather(town: str):
    response = await get_weather_metrics(town)
    return response
