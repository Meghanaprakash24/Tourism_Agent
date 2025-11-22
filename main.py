#!/usr/bin/env python3
"""
Tourism Multi-Agent System using CrewAI
"""

import os
import sys
from dotenv import load_dotenv
from crewai import Crew, LLM
from agents import TourismAgents
from tasks import TourismTasks

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Load environment
load_dotenv()

class TourismCrew:
    def __init__(self, destination):
        self.destination = destination
        
        # Check if using Ollama (free local option)
        use_ollama = os.getenv("USE_OLLAMA", "false").lower() == "true"
        
        if use_ollama:
            # Use Ollama - completely free, runs locally
            self.llm = LLM(
                model=os.getenv("OLLAMA_MODEL", "llama3.2"),
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
                api_key="ollama",  # Ollama doesn't require real API key
                temperature=0.3,
                max_tokens=2000
            )
        else:
            # Use OpenRouter (requires credits)
            self.llm = LLM(
                model=os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo"),
                temperature=0.3,
                base_url=os.getenv("OPENROUTER_BASE_URL"),
                api_key=os.getenv("OPEN_API_KEY"),
                max_tokens=1000
            )
        
    def run(self):
        # Initialize agents and tasks
        agents = TourismAgents(self.llm)
        tasks = TourismTasks()
        
        # Create agents
        parent_agent = agents.create_parent_agent()
        weather_agent = agents.create_weather_agent()
        places_agent = agents.create_places_agent()
        
        # Create tasks
        coordination_task = tasks.create_coordination_task(parent_agent, self.destination)
        weather_task = tasks.create_weather_task(weather_agent, self.destination, "{{coordination_task.output}}")
        places_task = tasks.create_places_task(places_agent, self.destination, "{{coordination_task.output}}")
        final_report_task = tasks.create_final_report_task(parent_agent, self.destination)
        
        # Update task contexts - final report needs both weather and places info
        weather_task.context = [coordination_task]
        places_task.context = [coordination_task]
        final_report_task.context = [coordination_task, weather_task, places_task]
        
        # Create and run crew
        crew = Crew(
            agents=[parent_agent, weather_agent, places_agent],
            tasks=[coordination_task, weather_task, places_task, final_report_task],
            verbose=True
        )
        
        result = crew.kickoff()
        return result

def extract_destination(user_input):
    """Extract destination from user input"""
    # Simple extraction - can be enhanced with NLP
    keywords = ["going to", "visit", "travel to", "plan trip to"]
    for keyword in keywords:
        if keyword in user_input.lower():
            parts = user_input.lower().split(keyword)
            if len(parts) > 1:
                destination = parts[1].strip().split()[0].strip('.,!?')
                return destination.capitalize()
    return None

def main():
    try:
        # Check if destination provided as command line argument
        if len(sys.argv) > 1:
            destination = sys.argv[1]
            print(f"Planning your trip to {destination}...")
        else:
            print("Welcome to Tourism AI Assistant!")
            print("Tell me where you want to go (e.g., 'I'm going to Bangalore')")
            
            user_input = input("\nYou: ").strip()
            
            destination = extract_destination(user_input)
            if not destination:
                print("Please specify a destination (e.g., 'I'm going to Bangalore')")
                return
        
        print(f"\nPlanning your trip to {destination}...")
        
        crew = TourismCrew(destination)
        result = crew.run()
        
        print("\n" + "="*50)
        print("TRAVEL RECOMMENDATION")
        print("="*50)
        print(result)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()