import re

def validate_place_exists(geocoding_result):
    """Validate if place exists from geocoding result"""
    if 'error' in geocoding_result or not geocoding_result:
        return False
    return True

def format_weather_data(weather_data):
    """Format weather API response into user-friendly text"""
    if 'error' in weather_data:
        return "Weather information currently unavailable"
    
    current = weather_data.get('current', {})
    temp = current.get('temperature_2m', 'N/A')
    precip = current.get('precipitation_probability', 'N/A')
    
    return f"Currently {temp}°C with {precip}% chance of rain"

def format_places_data(places_data):
    """Format places API response into user-friendly list"""
    if 'error' in places_data or 'elements' not in places_data:
        return ["No attractions found or service unavailable"]
    
    attractions = []
    for element in places_data['elements'][:5]:  # Limit to 5
        if 'tags' in element and 'name' in element['tags']:
            attractions.append(element['tags']['name'])
    
    return attractions if attractions else ["Popular local attractions (details unavailable)"]