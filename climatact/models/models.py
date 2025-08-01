from pydantic import BaseModel, Field


class TomorrowMetrics(BaseModel):
    rainIntensity: float = Field(..., description="Rainfall intensity (mm/hr)")
    humidity: float = Field(..., description="Humidity in %")
    precipitationProbability: float = Field(..., description="Chance of Rain in %")
    temperature: float = Field(..., description="Temperature in Celsius")


class GoogleMetrics(BaseModel):
    description: str = Field(..., description="Weather Description (e.g., Cloudy)")
    humidity: float = Field(..., description="Humidity in %")
    precipitationProbability: float = Field(..., description="Chance of Rain in %")
    temperature: float = Field(..., description="Temperature in Celsius")

class OpenmeteoMetrics(BaseModel):
    temperature: float = Field(..., description="Temperature in Celcius")
    weathercode: int = Field(..., description="World Meteorological Organisation Weather Code")
    windspeed: float = Field(..., description="Speed of Wind in km/h")

class WeatherResponse(BaseModel):
    town: str = Field(..., description="Name of the Requested Town")
    tomorrow_io: TomorrowMetrics = Field(..., description="Weather metrics from Tomorrow.io API")
    google: GoogleMetrics = Field(..., description="Weather metrics from Google Weather API")
    openmeteo: OpenmeteoMetrics = Field(..., description="Weather metrics from Openmeteo API")
