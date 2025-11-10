# PowerShell script to set up and run the application

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "               Architecture Recommendation Agent              " -ForegroundColor Cyan  
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
try {
    $output = python --version
    Write-Host "OK $output" -ForegroundColor Green
}
catch {
    Write-Host "ERROR Python not found. Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
Write-Host "
[2/6] Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "OK Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "OK Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "
[3/6] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "OK Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host "
[4/6] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "OK Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "ERROR Error installing dependencies" -ForegroundColor Red
    exit 1
}

# Check for .env file
Write-Host "
[5/6] Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "OK .env file found" -ForegroundColor Green
} else {
    Write-Host "WARNING .env file not found. Creating from template..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
    }
    Write-Host "ERROR Please edit .env and add your GOOGLE_API_KEY before running the server!" -ForegroundColor Red
    Write-Host "Get your API key from: https://makersuite.google.com/app/apikey" -ForegroundColor Yellow
    exit 1
}

# Start the server
Write-Host "
[6/6] Starting FastAPI server..." -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server starting at: http://localhost:8000" -ForegroundColor Green
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host ""

python main.py
