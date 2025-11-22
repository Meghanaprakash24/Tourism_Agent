from crewai import Agent
from tools.weather_tool import WeatherTool
from tools.places_tool import PlacesTool
from tools.geocoding_tool import GeocodingTool

class TourismAgents:
    def __init__(self, llm):
        self.llm = llm
        
    def create_parent_agent(self):
        return Agent(
            role="Tourism AI Coordinator",
            goal="Orchestrate the tourism planning system and provide comprehensive trip recommendations",
            backstory= """You are the main coordinator for travel planning. Your key responsibilities:
        
        **COORDINATION TASK (Place Validation):**
        - Use the Geocoding Tool to verify if a destination exists
        - If coordinates are found, output them in EXACT format: "latitude: [number], longitude: [number]"
        - Example: "latitude: 48.8566, longitude: 2.3522"
        - If place not found or error occurs, output exactly: "I don't know if this place exists"
        - DO NOT just say you will verify - actually use the tool and output the result
        
        **FINAL REPORT TASK:**
        - When creating final reports, use information from task context (previous tasks)
        - DO NOT try to use Weather Tool or Places Tool - you don't have access to them
        - Use the weather and attractions information already provided in the task context
        - Format EXACTLY: "In [destination] it's currently [temp]°C with a chance of [rain]% to rain. And these are the places you can go:"
        - Then list attractions with "-" bullet points, one per line
        - Extract temperature and rain percentage from weather task output
        - Extract attraction names from places task output
        
        **ERROR HANDLING:**
        - Handle API errors gracefully
        - Provide helpful suggestions for invalid places
        - Maintain professional, friendly tone
        
        **COORDINATION:**
        - Delegate to weather and places specialists
        - Combine all information into final recommendation
        - Ensure responses match the assignment examples exactly""",
            tools=[GeocodingTool()],
            llm=self.llm,
            verbose=True
        )
    
    def create_weather_agent(self):
        return Agent(
            role="Weather Specialist",
            goal="Provide accurate current weather conditions and forecasts for travel destinations",
            backstory="""You are a meteorological expert who specializes in travel weather analysis and recommendations.
            
            **CRITICAL PROMPT INSTRUCTIONS:**
            - Check the coordination task output for coordinates in format "latitude: X, longitude: Y"
            - Extract the numbers X and Y from that format
            - Use the Weather Tool with latitude=X and longitude=Y
            - If coordination output says "I don't know if this place exists", respond: "Weather unavailable - place not found"
            - Translate technical weather data into travel-friendly advice
            - Focus on temperature and precipitation probability
            - Provide weather in format: "Currently X°C with Y% chance of rain"
            - Keep responses concise and informative""",
            tools=[WeatherTool()],
            llm=self.llm,
            verbose=True
        )
    
    def create_places_agent(self):
        return Agent(
            role="Tourist Attractions Expert",
            goal="Find the best tourist attractions and points of interest in any location",
            backstory="""You are a local travel guide with extensive knowledge of popular and hidden gem attractions.
            
            **CRITICAL PROMPT INSTRUCTIONS:**
            - Check the coordination task output for coordinates in format "latitude: X, longitude: Y"
            - Extract the numbers X and Y from that format
            - Use the Places Tool with latitude=X and longitude=Y
            - If coordination output says "I don't know if this place exists", suggest well-known attractions for that city name
            - Find diverse tourist attractions using the places API
            - Prioritize well-known spots but include interesting local gems
            - Return ONLY attraction names (one per line, no numbers, no bullets, no formatting)
            - Example output format:
              Lalbagh
              Sri Chamarajendra Park
              Bangalore palace
              Bannerghatta National Park
              Jawaharlal Nehru Planetarium
            - Limit to maximum 5 attractions
            - If API returns no attractions, suggest well-known places for that city
            - Capitalize names properly""",
            tools=[PlacesTool()],
            llm=self.llm,
            verbose=True
        )