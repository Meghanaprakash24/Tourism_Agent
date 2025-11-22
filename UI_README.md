# 🌍 Tourism AI Assistant - Modern Web UI

A beautiful, modern web interface for the Multi-Agent Tourism System built with Streamlit.

## 🚀 Quick Start

### 1. Install Dependencies

Make sure you have all dependencies installed:

```bash
# Activate virtual environment (if using one)
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate      # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Make sure your `.env` file is set up with your API keys:

```env
OPEN_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-3.5-turbo

# OR use Ollama (free, local)
USE_OLLAMA=false
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434/v1
```

### 3. Run the Web UI

```bash
# Activate virtual environment first
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Run Streamlit app
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 🎨 Features

- **Modern, Beautiful UI**: Gradient colors, smooth animations, and clean design
- **Easy to Use**: Simple input form with example destinations
- **Real-time Processing**: See AI agents working in real-time
- **Structured Results**: Weather and attractions displayed separately
- **Responsive Design**: Works on desktop and mobile devices

## 📱 Usage

1. **Enter Destination**: Type a city name in the input field
2. **Click "Plan My Trip"**: The AI agents will coordinate to gather information
3. **View Results**: 
   - Current weather information
   - List of tourist attractions
   - Complete travel recommendation

## 🎯 Example Destinations

Try these popular destinations:
- Paris
- Bangalore
- Tokyo
- New York

## 💡 Tips

- Use full city names for better results
- Be specific (e.g., "New York" instead of "NY")
- The system works best with major cities

## 🔧 Troubleshooting

### Port Already in Use
If port 8501 is busy, use a different port:
```bash
streamlit run app.py --server.port 8502
```

### API Errors
- Make sure your API key has credits
- Or set up Ollama for free local AI
- Check your `.env` file configuration

### Module Not Found
Make sure you've activated your virtual environment and installed all dependencies:
```bash
pip install -r requirements.txt
```

## 🎨 Customization

You can customize the UI by editing `app.py`:
- Colors: Modify the CSS gradient colors
- Layout: Adjust column widths
- Styling: Change CSS classes

Enjoy planning your trips! 🌍✈️

