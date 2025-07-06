import os
import httpx
from climatact.services.geo_service import get_coordinates
from climatact.helper.response_handler import handler

async def get_weather_metrics(town: str) -> dict:
    TOMORROW_API_KEY = os.environ.get("TOMORROW_API_KEY")
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

    lat, lon = get_coordinates(town).get("lat"), get_coordinates(town).get("lon")

    tomorrow_url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={TOMORROW_API_KEY}"
    google_url = f"https://weather.googleapis.com/v1/currentConditions:lookup?key={GOOGLE_API_KEY}&location.latitude={lat}&location.longitude={lon}"

    headers = {
        "accept": "application/json",
        "accept-encoding": "deflate, gzip, br"
    }

    async with httpx.AsyncClient() as client:
        tomorrow_response = await client.get(tomorrow_url, headers=headers)
        google_response = await client.get(google_url)

    return handler(town, tomorrow_response, google_response)
