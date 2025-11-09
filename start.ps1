# PowerShell script to set up and run the application

Write-Host "╔═════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              Architecture Recommendation Agent              ║" -ForegroundColor Cyan
Write-Host "╚═════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
try {
  $pythonVersion = python --version 2>&1
  Write-Host "✓ $pythonVersion" -ForegroundColor Green
}
catch {
  Write-Host "✗ Python not found. Please install Python 3.9 or higher." -ForegroundColor Red
  exit 1
}

# Check if virtual environment exists
Write-Host "`n[2/6] Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
  Write-Host "✓ Virtual environment found" -ForegroundColor Green
}
else {
  Write-Host "Creating virtual environment..." -ForegroundColor Yellow
  python -m venv venv
  Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`n[3/6] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host "`n[4/6] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
  Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
}
else {
  Write-Host "✗ Error installing dependencies" -ForegroundColor Red
  exit 1
}

# Check for .env file
Write-Host "`n[5/6] Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
  Write-Host "✓ .env file found" -ForegroundColor Green
}
else {
  Write-Host "⚠ .env file not found. Creating from template..." -ForegroundColor Yellow
  Copy-Item ".env.example" ".env"
  Write-Host "✗ Please edit .env and add your GOOGLE_API_KEY before running the server!" -ForegroundColor Red
  Write-Host "Get your API key from: https://makersuite.google.com/app/apikey" -ForegroundColor Yellow
  exit 1
}

# Start the server
Write-Host "`n[6/6] Starting FastAPI server..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Server starting at: http://localhost:8000" -ForegroundColor Green
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

python main.py
