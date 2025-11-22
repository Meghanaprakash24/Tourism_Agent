# Multi-Agent Tourism System

A sophisticated multi-agent system built with CrewAI that helps plan trips by providing weather information and tourist attractions for any destination.

## 🚀 Features

- **Multi-Agent Architecture**: Coordinated agents for weather, places, and trip planning
- **Weather Information**: Current conditions and forecasts using Open-Meteo API
- **Tourist Attractions**: Finds popular attractions using OpenStreetMap data
- **Geocoding**: Validates destinations and gets coordinates
- **Intelligent Coordination**: Parent agent orchestrates all tasks

## 📋 Prerequisites

- **Python 3.10 to 3.13** (CrewAI does not support Python 3.14 yet)
- **LLM Access** - Choose ONE option:
  - **Option 1 (Recommended - FREE):** Ollama (runs locally, no API keys needed)
  - **Option 2:** OpenRouter API key (requires credits)
  - **Option 3:** Other free APIs (Groq, Hugging Face, etc.)

**⚠️ Important:** If you have Python 3.14, you'll need to install Python 3.13 or earlier. You can:
- Download Python 3.13 from [python.org](https://www.python.org/downloads/)
- Use a virtual environment with Python 3.13
- Or use pyenv to manage multiple Python versions

**💡 FREE Option:** See [SETUP_FREE.md](SETUP_FREE.md) for complete guide on using Ollama (100% free, no API keys!)

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Environment File

Create a `.env` file in the project root. Choose ONE option:

#### Option A: Ollama (FREE - Recommended)
```env
# Ollama Configuration (100% Free, No API Keys!)
USE_OLLAMA=true
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434/v1
```

**Setup Ollama:**
1. Install from: https://ollama.ai/download
2. Run: `ollama pull llama3.2`
3. Start: `ollama serve` (keep running)
4. See [SETUP_FREE.md](SETUP_FREE.md) for details

#### Option B: OpenRouter (Requires Credits)
```env
# OpenRouter Configuration
USE_OLLAMA=false
OPEN_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=openai/gpt-3.5-turbo
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

**How to get OpenRouter API Key:**
1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for an account
3. Go to Keys section and create a new API key
4. Copy the key to your `.env` file

### 3. Verify Installation

Check that all dependencies are installed:
```bash
python -c "import crewai; print('CrewAI installed successfully')"
```

## 🎯 Usage

### Run the Application

```bash
python main.py
```

### Example Interaction

```
🌍 Welcome to Tourism AI Assistant!
Tell me where you want to go (e.g., 'I'm going to Bangalore')

🧑 You: I'm going to Paris

🔄 Planning your trip to Paris...
```

The system will:
1. Validate the destination exists
2. Get current weather conditions
3. Find popular tourist attractions
4. Generate a comprehensive travel recommendation

## 🏗️ Project Structure

```
Multi-agent toursim sys/
├── main.py              # Main entry point and user interface
├── agents.py            # Agent definitions (Coordinator, Weather, Places)
├── tasks.py             # Task definitions for each agent
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
└── tools/
    ├── geocoding_tool.py    # Geocoding API integration
    ├── weather_tool.py      # Weather API integration
    └── places_tool.py       # Tourist attractions API integration
```

## 🔌 API Services Used

- **OpenRouter**: LLM access (requires API key)
- **Open-Meteo**: Weather data (free, no key needed)
- **Nominatim (OpenStreetMap)**: Geocoding (free, no key needed)
- **Overpass API**: Tourist attractions (free, no key needed)

## 🧪 Testing

### Test Individual Components

```python
# Test geocoding
from tools.geocoding_tool import GeocodingTool
tool = GeocodingTool()
result = tool._run("Paris")
print(result)

# Test weather
from tools.weather_tool import WeatherTool
tool = WeatherTool()
result = tool._run(48.8566, 2.3522)  # Paris coordinates
print(result)

# Test places
from tools.places_tool import PlacesTool
tool = PlacesTool()
result = tool._run(48.8566, 2.3522)  # Paris coordinates
print(result)
```

## 🐛 Troubleshooting

### Common Issues

1. **"OPEN_API_KEY not found"**
   - Make sure `.env` file exists in project root
   - Verify the key name matches exactly: `OPEN_API_KEY`

2. **"Module not found"**
   - Run `pip install -r requirements.txt`
   - Make sure you're in the correct directory

3. **API Rate Limits**
   - OpenRouter: Check your account limits
   - Nominatim: Add a User-Agent header if needed
   - Overpass: May have rate limits for heavy usage

4. **"I don't know if this place exists"**
   - Try more specific location names (e.g., "Paris, France" instead of "Paris")
   - Check spelling of the destination

## 🚀 Next Steps & Improvements

### Immediate Next Steps:
1. ✅ **Set up `.env` file** with your OpenRouter API key
2. ✅ **Test the system** with a known destination
3. ✅ **Verify all APIs are working**

### Potential Enhancements:
- [ ] Add hotel/accommodation recommendations
- [ ] Include restaurant suggestions
- [ ] Add budget estimation
- [ ] Create a web interface (Flask/FastAPI)
- [ ] Add travel itinerary generation
- [ ] Include transportation options
- [ ] Add historical/seasonal weather trends
- [ ] Implement caching for API calls
- [ ] Add error logging and monitoring
- [ ] Create unit tests
- [ ] Add support for multiple languages
- [ ] Include travel warnings/advisories

## 📝 Notes

- The system uses free APIs for geocoding, weather, and places (no API keys needed)
- Only OpenRouter requires an API key for LLM functionality
- All APIs have rate limits - be mindful of heavy usage
- The system validates destinations before proceeding with recommendations

## 🤝 Contributing

Feel free to extend this system with additional features or improvements!

## 📄 License

This project is open source and available for educational purposes.

