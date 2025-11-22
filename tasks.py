from crewai import Task
from tools.geocoding_tool import GeocodingTool

class TourismTasks:
    def __init__(self):
        self.geocoding_tool = GeocodingTool()
    
    def create_coordination_task(self, agent, destination):
        return Task(
            description=f"""Verify if the place "{destination}" exists and get its coordinates.
            
            **CRITICAL INSTRUCTIONS:**
            1. Use the Geocoding Tool to search for "{destination}"
            2. If the tool returns coordinates (lat and lon), output them in this exact format:
               "latitude: [lat], longitude: [lon]"
               Example: "latitude: 48.8566, longitude: 2.3522"
            3. If the tool returns an error or "Place not found", output exactly:
               "I don't know if this place exists"
            4. DO NOT just say you will verify - actually use the tool and output the result
            
            **IMPORTANT:** Your output must be either coordinates in the format above, or the error message. This output will be used by other agents.""",
            expected_output="Coordinates in format 'latitude: X, longitude: Y' OR error message 'I don't know if this place exists'",
            agent=agent,
            tools=[self.geocoding_tool]
        )
    
    def create_weather_task(self, agent, destination, coordinates):
        return Task(
            description=f"""Get current weather and forecast for {destination}.
            
            **CRITICAL INSTRUCTIONS:**
            1. First, check the coordination task output: {coordinates}
            2. If it says "I don't know if this place exists", respond: "Weather unavailable - place not found"
            3. If it contains coordinates in format "latitude: X, longitude: Y":
               - Extract the latitude and longitude numbers
               - Use the Weather Tool with these coordinates
               - Format response: "Currently X°C with Y% chance of rain"
            4. If weather data unavailable, say so clearly
            5. Keep it brief and travel-focused
            
            **Example:** If coordination output is "latitude: 48.8566, longitude: 2.3522", 
            use Weather Tool with latitude=48.8566 and longitude=2.3522""",
            expected_output="Current weather conditions in format 'Currently X°C with Y% chance of rain' OR error message",
            agent=agent,
            context=[]
        )
    
    def create_places_task(self, agent, destination, coordinates):
        return Task(
            description=f"""Find up to 5 popular tourist attractions in {destination}.
            
            **CRITICAL INSTRUCTIONS:**
            1. First, check the coordination task output: {coordinates}
            2. If it says "I don't know if this place exists", provide well-known attractions for that city name
            3. If it contains coordinates in format "latitude: X, longitude: Y":
               - Extract the latitude and longitude numbers
               - Use the Places Tool with these coordinates
               - If the tool returns an error (check for "error" key in response), suggest well-known attractions for {destination}
               - If the tool returns attractions, extract the names from elements[].tags.name
               - Return up to 5 attractions
            4. Format as simple list of attraction names only (one per line, no numbers, no bullets)
            5. Example format:
               Lalbagh
               Sri Chamarajendra Park
               Bangalore palace
               Bannerghatta National Park
               Jawaharlal Nehru Planetarium
            6. If Places Tool returns error or no attractions found, suggest well-known attractions for {destination}
            7. Ensure all names are properly capitalized
            8. Return ONLY the names, ready to be formatted as bullet points later
            9. Always provide at least 3-5 attractions, even if API fails
            
            **Example:** If coordination output is "latitude: 48.8566, longitude: 2.3522", 
            use Places Tool with latitude=48.8566 and longitude=2.3522""",
            expected_output="List of up to 5 tourist attraction names (one per line, no numbers or bullets) OR well-known attractions if place not found",
            agent=agent,
            context=[]
        )
    
    def create_final_report_task(self, agent, destination):
        return Task(
            description=f"""Combine all information about {destination} into a travel recommendation.
            
            **CRITICAL: Use the context from previous tasks - DO NOT try to use tools.**
            **The weather and attractions information is already available in the task context.**
            
            **EXACT OUTPUT FORMAT REQUIRED:**
            Start with: "In [destination] it's currently [temperature]°C with a chance of [rain_percentage]% to rain. And these are the places you can go:"
            
            Then list attractions as bullet points (use "-" for each item):
            - [Attraction 1]
            - [Attraction 2]
            - [Attraction 3]
            - etc.
            
            **SPECIFIC INSTRUCTIONS:**
            1. Extract temperature from weather task context (look for "Currently X°C" or temperature value)
            2. Extract rain percentage from weather task context (look for "Y% chance of rain" or precipitation probability)
            3. Extract attraction names from places task context (use the exact names provided)
            4. Format EXACTLY as shown above - use "it's currently" not "the current weather is"
            5. Use "with a chance of X% to rain" format (not "with X% chance of rain")
            6. List attractions with "-" bullet points, one per line
            7. Capitalize attraction names properly
            8. If place doesn't exist (from coordination task), clearly state "I don't know if this place exists"
            
            **EXAMPLE OUTPUT:**
            "In Bangalore it's currently 24°C with a chance of 35% to rain. And these are the places you can go:
            
            - Lalbagh
            - Sri Chamarajendra Park
            - Bangalore palace
            - Bannerghatta National Park
            - Jawaharlal Nehru Planetarium"
            
            **DO NOT try to use Weather Tool or Places Tool - use the information from task context instead.**""",
            expected_output="Travel recommendation in exact format: 'In [city] it's currently [temp]°C with a chance of [rain]% to rain. And these are the places you can go:' followed by bulleted list",
            agent=agent,
            context=[]  # Will be set in main.py
        )