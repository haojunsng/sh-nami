import os
import httpx
from fastapi import HTTPException
from climatact.services.geo_service import get_coordinates
from climatact.helper.response_handler import handler

async def get_weather_metrics(town: str) -> dict:
    
    try:
        TOMORROW_API_KEY = os.environ["TOMORROW_API_KEY"]
        GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
    except KeyError as e:
        missing_key = e.args[0]
        raise RuntimeError(f"Environment variable {missing_key} is required but not found.") from e


    lat, lon = get_coordinates(town).get("lat"), get_coordinates(town).get("lon")

    tomorrow_url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={TOMORROW_API_KEY}"
    google_url = f"https://weather.googleapis.com/v1/currentConditions:lookup?key={GOOGLE_API_KEY}&location.latitude={lat}&location.longitude={lon}"
    openmeteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    headers = {
        "accept": "application/json",
        "accept-encoding": "deflate, gzip, br"
    }
    try:
        async with httpx.AsyncClient() as client:
            tomorrow_response = await client.get(tomorrow_url, headers=headers)
            google_response = await client.get(google_url)
            openmeteo_response = await client.get(openmeteo_url)

        tomorrow_response.raise_for_status()
        google_response.raise_for_status()
        openmeteo_response.raise_for_status()
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Upstream service returned error: {e.response.status_code}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=504, detail="Unable to reach weather service.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    return handler(town, tomorrow_response, google_response, openmeteo_response)
