import requests
import os
from typing import Optional, Dict

def weather_tool(city: Optional[str] = None,
    location: Optional[Dict] = None):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {"error": "OPENWEATHER_API_KEY environment variable is required. Please set it in your .env file."}
    if city:
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    elif location and "lat"in location and "lon" in location:
        url=f"https://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lon']}&appid={api_key}"
    else:
        return { "message":"Please provide a city name or give location access to get the weather."}
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        print(data["main"])
        
        if "main" in data:
            # Convert from Kelvin to Celsius
            temp_kelvin = data["main"]["temp"]
            temp_celsius = round(temp_kelvin - 273.15, 2)
            return {
            "city": city if city else data.get("name"),
            "temperature": temp_celsius,
            "temperature_unit": "celsius",
            "humidity": data["main"]["humidity"],
            "humidity_label": (
                "dry" if data["main"]["humidity"] < 30
                else "comfortable" if data["main"]["humidity"] < 60
                else "humid"),
            "pressure": data["main"]["pressure"],
            "pressure_label": (
                "low" if data["main"]["pressure"] < 1000
                else "high" if data["main"]["pressure"] > 1020
                else "normal"),
            "condition": data["weather"][0]["description"]
        }
        else:
            return {"error": data.get("message", "Unable to fetch weather data")}
    
    except Exception as e:
        return {"status": "ERROR", "reason": f"Network/API error: {e}"}

