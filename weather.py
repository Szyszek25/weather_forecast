"""Shared weather utilities for the command line and GUI apps."""

import requests
from urllib.parse import quote

BASE_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def get_lat_lon(city_name: str):
    """Return latitude and longitude for a given city using Nominatim."""
    url = f"https://nominatim.openstreetmap.org/search?q={quote(city_name)}&format=json&limit=1"
    try:
        response = requests.get(url, headers={"User-Agent": "weather-app"})
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except requests.RequestException:
        pass
    return None, None


def get_current_weather(lat: float, lon: float):
    """Fetch current weather data from Open-Meteo."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
    }
    response = requests.get(BASE_FORECAST_URL, params=params)
    response.raise_for_status()
    return response.json()


def get_daily_forecast(lat: float, lon: float, days: int = 3):
    """Fetch daily forecast for a given number of days."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": "auto",
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
    }
    response = requests.get(BASE_FORECAST_URL, params=params)
    response.raise_for_status()
    data = response.json()
    if days > 0:
        # Limit results to requested number of days if API returned more
        for key in data.get("daily", {}):
            data["daily"][key] = data["daily"][key][:days]
    return data
