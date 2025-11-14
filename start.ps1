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
}
else {
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
}
else {
    Write-Host "ERROR Error installing dependencies" -ForegroundColor Red
    exit 1
}

# Check for .env file
Write-Host "
[5/6] Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "OK .env file found" -ForegroundColor Green
}
else {
    Write-Host "WARNING .env file not found. Creating from template..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
    }
    Write-Host "ERROR Please edit .env and add your GOOGLE_API_KEY before running the server!" -ForegroundColor Red
    Write-Host "Get your API key from: https://makersuite.google.com/app/apikey" -ForegroundColor Yellow
    exit 1
}

# Check if Node.js is installed
Write-Host "
[6/8] Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "OK Node.js $nodeVersion" -ForegroundColor Green
}
catch {
    Write-Host "ERROR Node.js not found. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check and install frontend dependencies
Write-Host "
[7/8] Checking frontend dependencies..." -ForegroundColor Yellow
Push-Location "view"
if (Test-Path "node_modules") {
    Write-Host "OK Frontend dependencies found" -ForegroundColor Green
}
else {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK Frontend dependencies installed" -ForegroundColor Green
    }
    else {
        Write-Host "ERROR Error installing frontend dependencies" -ForegroundColor Red
        Pop-Location
        exit 1
    }
}
Pop-Location

# Start both servers
Write-Host "
[8/8] Starting Backend and Frontend servers..." -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Green
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop both servers" -ForegroundColor Yellow
Write-Host ""
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host ""

# Start backend in background
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    & ".\venv\Scripts\Activate.ps1"
    python main.py
}

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend
Push-Location "view"
try {
    npm run dev
}
finally {
    Pop-Location
    # Stop backend when frontend stops
    Stop-Job -Job $backendJob
    Remove-Job -Job $backendJob
}
