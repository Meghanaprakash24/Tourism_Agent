import requests
from crewai.tools import BaseTool
from pydantic import Field

class PlacesTool(BaseTool):
    name: str = "Places Tool"
    description: str = "Get tourist attractions using Overpass API"
    
    def _run(self, latitude: float, longitude: float) -> dict:
        # Overpass query to find tourist attractions within 10km radius
        # Fixed query syntax - limit is applied via (around:radius) and out count
        overpass_query = f"""[out:json][timeout:25];
(
  node["tourism"~"attraction|museum|artwork|viewpoint|theme_park"]["name"](around:10000,{latitude},{longitude});
  way["tourism"~"attraction|museum|artwork|viewpoint|theme_park"]["name"](around:10000,{latitude},{longitude});
  relation["tourism"~"attraction|museum|artwork|viewpoint|theme_park"]["name"](around:10000,{latitude},{longitude});
);
out body 5;
out skel qt;"""
        
        url = "https://overpass-api.de/api/interpreter"
        headers = {
            'User-Agent': 'TourismAI/1.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = requests.post(url, data={'data': overpass_query}, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Check if response is actually JSON
            if not response.text or response.text.strip() == '':
                return {"error": "Empty response from Overpass API"}
            
            # Try to parse JSON
            try:
                data = response.json()
            except ValueError as json_error:
                return {"error": f"Invalid JSON response: {str(json_error)}. Response: {response.text[:200]}"}
            
            # Filter and simplify the response to only essential data
            if 'elements' in data and data['elements']:
                simplified = {
                    'elements': []
                }
                for element in data['elements'][:5]:  # Limit to 5
                    # Handle different element types (node, way, relation)
                    simplified_element = {
                        'type': element.get('type'),
                        'id': element.get('id'),
                        'tags': {}
                    }
                    
                    # Get coordinates - nodes have lat/lon directly, ways/relations need center
                    if 'lat' in element and 'lon' in element:
                        simplified_element['lat'] = element.get('lat')
                        simplified_element['lon'] = element.get('lon')
                    elif 'center' in element:
                        simplified_element['lat'] = element['center'].get('lat')
                        simplified_element['lon'] = element['center'].get('lon')
                    
                    # Only include name tag
                    if 'tags' in element and 'name' in element['tags']:
                        simplified_element['tags']['name'] = element['tags']['name']
                        simplified['elements'].append(simplified_element)
                
                # Return simplified data or empty if no names found
                if simplified['elements']:
                    return simplified
                else:
                    return {"error": "No attractions with names found in the area"}
            
            # If no elements, return empty result
            return {"elements": []}
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Places API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}