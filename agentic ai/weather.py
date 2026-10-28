#!/usr/bin/env python3
"""
Simple city weather reporter using the free Open-Meteo API.
No API key or third-party Python packages are required.

Run:
    python weather.py
Then enter a city name when prompted.
"""

import json
import urllib.error
import urllib.parse
import urllib.request


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_json(url):
    """Fetch JSON from a URL with a helpful timeout and user agent."""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "CityWeatherReporter/1.0"}
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def find_city(city_name):
    params = urllib.parse.urlencode({
        "name": city_name,
        "count": 5,
        "language": "en",
        "format": "json",
    })
    data = get_json(f"{GEOCODING_URL}?{params}")
    return data.get("results", [])


def get_weather(latitude, longitude):
    params = urllib.parse.urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "is_day,precipitation,weather_code,wind_speed_10m,wind_direction_10m"
        ),
        "daily": (
            "weather_code,temperature_2m_max,temperature_2m_min,"
            "precipitation_probability_max,sunrise,sunset"
        ),
        "timezone": "auto",
        "forecast_days": 1,
    })
    return get_json(f"{WEATHER_URL}?{params}")


def print_report(place, weather):
    current = weather["current"]
    daily = weather["daily"]
    code = current.get("weather_code")
    description = WEATHER_CODES.get(code, f"Unknown weather (code {code})")
    today_code = daily["weather_code"][0]