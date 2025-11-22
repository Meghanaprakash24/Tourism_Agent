# PowerShell script to run the Tourism AI Assistant Web UI
Write-Host "Starting Tourism AI Assistant Web UI..." -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Activate virtual environment if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1
    Write-Host "Virtual environment activated." -ForegroundColor Green
} else {
    Write-Host "No virtual environment found. Using system Python." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Starting Streamlit..." -ForegroundColor Cyan
Write-Host "The app will open in your browser automatically." -ForegroundColor Green
Write-Host ""

# Run Streamlit
streamlit run app.py

