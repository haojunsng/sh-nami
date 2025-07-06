import json
from operator import itemgetter
from climatact.models.models import TomorrowMetrics, GoogleMetrics, WeatherResponse

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

def handler(town, tomorrow_response, google_response):
    tomorrow_metrics = tomorrow_handler(tomorrow_response)
    google_metrics = google_handler(google_response)
    return WeatherResponse(
        town=town,
        tomorrow_io=tomorrow_metrics,
        google=google_metrics
    )
