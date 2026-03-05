"""
weather_api.py
Fetches live weather data from OpenWeatherMap API.
Free API key from: https://openweathermap.org/api
"""

import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def _parse_response(data: dict) -> dict:
    """Parse raw OWM API response into app-ready dict."""
    weather_main = data["weather"][0]["main"]  # e.g. "Rain", "Clear", "Snow", "Clouds"
    temp_kelvin = data["main"]["temp"]
    clouds_all = data["clouds"]["all"]  # percentage
    rain_1h = data.get("rain", {}).get("1h", 0.0)
    snow_1h = data.get("snow", {}).get("1h", 0.0)
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    description = data["weather"][0]["description"].capitalize()
    city_name = data.get("name", "Unknown")
    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]

    return {
        "temp": round(temp_kelvin, 2),
        "weather_main": weather_main,
        "rain_1h": round(rain_1h, 3),
        "snow_1h": round(snow_1h, 3),
        "clouds_all": clouds_all,
        "humidity": humidity,
        "wind_speed": round(wind_speed, 2),
        "description": description,
        "city_name": city_name,
        "lat": lat,
        "lon": lon,
    }


def get_weather_by_city(city: str, api_key: str) -> dict | None:
    """
    Fetch current weather for a city name.
    Returns parsed weather dict or None on failure.
    """
    api_key = api_key.strip()
    try:
        params = {
            "q": city,
            "appid": api_key,
            "units": "standard",  # Kelvin for temp
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return _parse_response(response.json())
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            raise ValueError("❌ Invalid API Key. Note: New OpenWeatherMap keys can take 1-2 hours to activate. If your key is brand new, please try again later.")
        elif response.status_code == 404:
            raise ValueError(f"❌ City '{city}' not found. Please check the spelling.")
        else:
            raise ValueError(f"❌ Weather API Error: {response.json().get('message', str(e))}")
    except Exception as e:
        raise ValueError(f"❌ Connectivity Error: {str(e)}")


def get_weather_by_coords(lat: float, lon: float, api_key: str) -> dict | None:
    """
    Fetch current weather by latitude/longitude.
    Returns parsed weather dict or None on failure.
    """
    api_key = api_key.strip()
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "standard",
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return _parse_response(response.json())
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            raise ValueError("❌ Invalid API Key. Note: New keys can take 1-2 hours to activate.")
        else:
            raise ValueError(f"❌ Weather API Error: {response.json().get('message', str(e))}")
    except Exception as e:
        raise ValueError(f"❌ Connectivity Error: {str(e)}")
