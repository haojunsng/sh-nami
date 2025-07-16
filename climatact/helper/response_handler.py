import json
from operator import itemgetter
from climatact.models.models import TomorrowMetrics, GoogleMetrics, OpenmeteoMetrics, WeatherResponse

def tomorrow_handler(response):
    text = json.loads(response.text)
    metrics = text.get("data").get("values")
    rainIntensity, humidity, precipitationProbability, temperature = itemgetter("rainIntensity", "humidity", "precipitationProbability", "temperature")(metrics)
    return TomorrowMetrics(
        rainIntensity=rainIntensity,
        humidity=humidity,
        precipitationProbability=precipitationProbability,
        temperature=temperature
    )

def google_handler(response):
    text = json.loads(response.text)
    desc = text.get("weatherCondition").get("description").get("text")
    temperature = text.get("temperature").get("degrees")
    humidity = text.get("relativeHumidity")
    precipitationProbability = text.get("precipitation").get("probability").get("percent")
    return GoogleMetrics(
        description=desc,
        humidity=humidity,
        precipitationProbability=precipitationProbability,
        temperature=temperature
    )

def openmeteo_handler(response):
    text = json.loads(response.text)
    temperature = text.get("current_weather").get("temperature")
    weathercode = text.get("current_weather").get("weathercode")
    windspeed = text.get("current_weather").get("windspeed")
    return OpenmeteoMetrics(
        temperature=temperature,
        weathercode=weathercode,
        windspeed=windspeed
    )

def handler(town, tomorrow_response, google_response, openmeteo_response):
    tomorrow_metrics = tomorrow_handler(tomorrow_response)
    google_metrics = google_handler(google_response)
    openmeteo_metrics = openmeteo_handler(openmeteo_response)
    return WeatherResponse(
        town=town,
        tomorrow_io=tomorrow_metrics,
        google=google_metrics,
        openmeteo=openmeteo_metrics
    )
