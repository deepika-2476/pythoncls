
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #74b9ff, #6c5ce7);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }
        .card {
            background: rgba(255,255,255,0.18);
            padding: 35px;
            border-radius: 20px;
            width: 340px;
            max-width: 85%;
            text-align: center;
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        }
        h1 { margin-top: 0; }
        input, button {
            box-sizing: border-box;
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: none;
            border-radius: 8px;
            font-size: 16px;
        }
        button {
            background: #0984e3;
            color: white;
            cursor: pointer;
        }
        button:hover { background: #0652dd; }
        .result {
            margin-top: 20px;
            background: rgba(0,0,0,0.12);
            border-radius: 12px;
            padding: 15px;
        }
        .temp { font-size: 42px; font-weight: bold; }
        .error { color: #fff0a8; }
    </style>
</head>
<body>
    <div class="card">
        <h1>☀️ Weather App</h1>
        <p>Check the weather in any city</p>

        <form method="POST">
            <input type="text" name="city"
                   placeholder="Enter city name"
                   value="{{ city }}" required>
            <button type="submit">Get Weather</button>
        </form>

        {% if weather %}
        <div class="result">
            <h2>{{ weather.city }}</h2>
            <div class="temp">{{ weather.temp }}°C</div>
            <p>{{ weather.description }}</p>
            <p>💧 Humidity: {{ weather.humidity }}%</p>
            <p>💨 Wind: {{ weather.wind }} km/h</p>
        </div>
        {% endif %}

        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

def get_description(code):
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Foggy",
        51: "Light drizzle",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Light snow",
        80: "Rain showers",
        95: "Thunderstorm"
    }
    return descriptions.get(code, "Weather conditions unavailable")


@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        try:
            # Find the city coordinates
            geo_response = requests.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1, "language": "en"},
                timeout=10
            )
            geo_response.raise_for_status()
            places = geo_response.json().get("results", [])

            if not places:
                error = "City not found. Please try another city."
            else:
                place = places[0]
                latitude = place["latitude"]
                longitude = place["longitude"]

                # Get current weather
                response = requests.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "current": (
                            "temperature_2m,relative_humidity_2m,"
                            "apparent_temperature,is_day,weather_code,"
                            "wind_speed_10m"
                        ),
                        "timezone": "auto"
                    },
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()
                current = data["current"]

                location = place["name"]
                if place.get("country"):
                    location += ", " + place["country"]

                weather = {
                    "city": location,
                    "temp": current["temperature_2m"],
                    "humidity": current["relative_humidity_2m"],
                    "wind": current["wind_speed_10m"],
                    "description": get_description(
                        current["weather_code"]
                    )
                }

        except requests.RequestException:
            error = "Unable to fetch weather. Check your internet connection."
        except (KeyError, ValueError):
            error = "Weather data could not be processed."

    return render_template_string(
        HTML, city=city, weather=weather, error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
