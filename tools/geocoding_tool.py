import requests
from crewai.tools import BaseTool
from pydantic import Field

class GeocodingTool(BaseTool):
    name: str = "Geocoding Tool"
    description: str = "Get coordinates (latitude, longitude) for a place name using Nominatim API"
    
    def _run(self, place_name: str) -> dict:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': place_name,
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'TourismAI/1.0'
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                return {
                    'lat': float(data[0]['lat']),
                    'lon': float(data[0]['lon']),
                    'display_name': data[0]['display_name']
                }
            return {"error": "Place not found"}
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except (ValueError, KeyError, IndexError) as e:
            return {"error": f"Data parsing error: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}