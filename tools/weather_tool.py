import requests
from crewai.tools import BaseTool
from pydantic import Field

class WeatherTool(BaseTool):
    name: str = "Weather Tool"
    description: str = "Get current weather and forecast using Open-Meteo API"
    
    def _run(self, latitude: float, longitude: float) -> dict:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,precipitation_probability,weather_code',
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_max',
            'timezone': 'auto'
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            return data
        except Exception as e:
            return {"error": str(e)}