@echo off
echo Starting Tourism AI Assistant Web UI...
echo.
cd /d "%~dp0"
if exist "venv\Scripts\Activate.bat" (
    call venv\Scripts\Activate.bat
    echo Virtual environment activated.
) else (
    echo No virtual environment found. Using system Python.
)
echo.
echo Starting Streamlit...
streamlit run app.py
pause

