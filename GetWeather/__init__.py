import azure.functions as func
import requests
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Extract the latitude and longitude from the query parameters
    latitude = req.params.get('latitude')
    longitude = req.params.get('longitude')

    if not latitude or not longitude:
        return func.HttpResponse(
            "Please pass both latitude and longitude in the query string",
            status_code=400
        )

    # Call the Open-Meteo API
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
    response = requests.get(weather_url)
    data = response.json()

    if response.status_code == 200:
        return func.HttpResponse(json.dumps(data), mimetype="application/json")
    else:
        return func.HttpResponse(
            "Failed to fetch the weather data",
            status_code=response.status_code
        )
