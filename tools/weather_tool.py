import requests
import os
from typing import Optional, Dict

def weather_tool(city: Optional[str] = None,
    location: Optional[Dict] = None):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {"message": "OPENWEATHER_API_KEY environment variable is required. Please set it in your .env file."}
    if city:
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    elif location and "lat"in location and "lon" in location:
        url=f"https://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lon']}&appid={api_key}"
    else:
        return { "message":"Please provide a city name or give location access to get the weather."}
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
            return {
                "status": "ERROR",
                "message": "Please enter the full city name (e.g. New York instead of NYC)."
            }

        
        
    
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        #print(data["main"])
        
        if "main" in data:
            
            main = data["main"]

            # Temperatures
            temp_celsius = round(main.get("temp", 0) - 273.15, 2)
            feels_like_celsius = round(main.get("feels_like", 0) - 273.15, 2)

            # Humidity
            humidity = main.get("humidity", 0)
            if humidity < 30:
                humidity_label = "Dry"
            elif humidity <= 60:
                humidity_label = "Comfortable"
            else:
                humidity_label = "Humid"

            # Pressure
            pressure = main.get("pressure", 0)
            if pressure < 1000:
                pressure_label = "Low"
            elif pressure <= 1020:
                pressure_label = "Normal"
            else:
                pressure_label = "High"

         

            return {
                "City": city or data.get("name", "Unknown location"),
                "Temperature": f"{temp_celsius} °C",
                "Feels Like": f"{feels_like_celsius} °C",
                "Humidity": f"{humidity}%",
                "Humidity Label": humidity_label,
                "Pressure": f"{pressure} hPa",
                "Pressure Label": pressure_label,
                
            }

        else:
            return {"status": "ERROR",
                    "message": "Weather data unavailable for this location."}

 
           
    
    except requests.exceptions.RequestExceptione:
        return { "status": "ERROR",
            "message": "Unable to reach weather service. Please try again."}

