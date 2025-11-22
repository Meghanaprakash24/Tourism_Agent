#!/usr/bin/env python3
"""
Modern Web UI for Tourism Multi-Agent System
Built with Streamlit
"""

import streamlit as st
import sys
import os
import re
from dotenv import load_dotenv
from crewai import Crew, LLM
from agents import TourismAgents
from tasks import TourismTasks

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Load environment
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🌍 Tourism AI Assistant",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .weather-info {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .attraction-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 3px solid #764ba2;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .example-button {
        background: #f0f2f6;
        color: #667eea;
        border: 2px solid #667eea;
    }
    .example-button:hover {
        background: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

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
            verbose=False  # Disable verbose for cleaner UI
        )
        
        result = crew.kickoff()
        return result

def parse_recommendation(result_text):
    """Parse the recommendation text to extract weather and attractions"""
    weather_info = None
    attractions = []
    
    # Convert to string if needed
    text = str(result_text)
    
    # Extract weather info
    import re
    weather_pattern = r'(\d+(?:\.\d+)?°C[^.]*(?:rain|precipitation|chance)[^.]*)'
    weather_matches = re.findall(weather_pattern, text, re.IGNORECASE)
    if weather_matches:
        weather_info = weather_matches[0].strip()
    else:
        # Fallback: look for temperature
        temp_pattern = r'(\d+(?:\.\d+)?°C[^.]*)'
        temp_matches = re.findall(temp_pattern, text)
        if temp_matches:
            weather_info = temp_matches[0].strip()
    
    # Extract attractions - look for numbered lists, bullet points, or structured lists
    lines = text.split('\n')
    in_attractions = False
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Check if we're in an attractions section
        if any(keyword in line.lower() for keyword in ['attraction', 'visit', 'places', 'landmark', 'tourist']):
            in_attractions = True
            continue
        
        # Extract numbered or bulleted items
        if in_attractions or line.startswith(('-', '•', '*', '1.', '2.', '3.', '4.', '5.')):
            # Clean up the line
            clean_line = re.sub(r'^[-•*\d.\s]+', '', line).strip()
            if clean_line and len(clean_line) > 10 and not clean_line.startswith('Here'):
                attractions.append(clean_line)
    
    # If no structured list found, try to extract from the full text
    if not attractions:
        # Look for sentences that might be attractions
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 200:
                if any(keyword in sentence.lower() for keyword in ['temple', 'museum', 'palace', 'park', 'garden', 'market', 'tower', 'cathedral']):
                    attractions.append(sentence)
    
    return weather_info, attractions[:10]  # Limit to 10 attractions

def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 Tourism AI Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Plan your perfect trip with AI-powered recommendations</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        st.markdown("---")
        st.info("**How it works:**\n\n1. Enter your destination\n2. AI agents coordinate to gather:\n   - Weather information\n   - Tourist attractions\n3. Get a complete travel recommendation")
        st.markdown("---")
        st.markdown("**💡 Tips:**\n- Use full city names (e.g., 'Paris', 'Bangalore')\n- Be specific for better results")
    
    # Initialize session state
    if 'selected_destination' not in st.session_state:
        st.session_state.selected_destination = None
    
    # Main content area
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Input form
        with st.form("tourism_form", clear_on_submit=False):
            # Pre-fill if example was clicked
            default_value = st.session_state.selected_destination if st.session_state.selected_destination else ""
            destination = st.text_input(
                "📍 Where do you want to go?",
                value=default_value,
                placeholder="e.g., Paris, Bangalore, Tokyo...",
                help="Enter the name of your travel destination"
            )
            
            submitted = st.form_submit_button("🚀 Plan My Trip", use_container_width=True)
        
        # Handle form submission
        destination_to_process = None
        if submitted:
            if destination:
                destination_to_process = destination
            else:
                st.error("❌ Please enter a destination!")
        elif st.session_state.selected_destination:
            destination_to_process = st.session_state.selected_destination
            st.session_state.selected_destination = None  # Reset after use
        
        # Process destination
        if destination_to_process:
            # Show loading state
            with st.spinner(f"🤖 Planning your trip to {destination_to_process}... This may take a minute."):
                try:
                    # Run the crew
                    crew = TourismCrew(destination_to_process)
                    result = crew.run()
                    
                    # Display results
                    st.success("✅ Trip planning complete!")
                    st.markdown("---")
                    
                    # Parse and display results
                    weather_info, attractions = parse_recommendation(str(result))
                    
                    # Weather section
                    if weather_info:
                        st.markdown("### 🌤️ Current Weather")
                        st.markdown(f'<div class="weather-info">{weather_info}</div>', unsafe_allow_html=True)
                    
                    # Attractions section
                    if attractions:
                        st.markdown("### 🎯 Tourist Attractions")
                        for i, attraction in enumerate(attractions, 1):
                            st.markdown(f'<div class="attraction-item"><strong>{i}.</strong> {attraction}</div>', unsafe_allow_html=True)
                    
                    # Full recommendation
                    st.markdown("---")
                    st.markdown("### 📋 Complete Recommendation")
                    st.markdown(f'<div class="result-box">{str(result)}</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Tip: Make sure your API key has credits, or set up Ollama for free local AI.")
        
        # Example destinations
        st.markdown("---")
        st.markdown("### 🌟 Try these destinations:")
        example_cols = st.columns(4)
        examples = ["Paris", "Bangalore", "Tokyo", "New York"]
        
        for i, example in enumerate(examples):
            with example_cols[i]:
                if st.button(example, key=f"example_{i}", use_container_width=True):
                    st.session_state.selected_destination = example
                    st.rerun()

if __name__ == "__main__":
    main()

