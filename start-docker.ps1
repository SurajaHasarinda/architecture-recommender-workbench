# PowerShell script to start the application with Docker

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "     Architecture Recommendation Agent - Docker Setup          " -ForegroundColor Cyan  
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "[1/4] Checking Docker installation..." -ForegroundColor Yellow
try {
    docker --version | Out-Null
    docker-compose --version | Out-Null
    Write-Host "✓ Docker and Docker Compose found" -ForegroundColor Green
}
catch {
    Write-Host "✗ Docker or Docker Compose not found!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check .env file
Write-Host "`n[2/4] Checking configuration..." -ForegroundColor Yellow
if (!(Test-Path ".env")) {
    Write-Host "✗ .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env file with GOOGLE_API_KEY" -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        Write-Host "Please edit .env and add your GOOGLE_API_KEY" -ForegroundColor Yellow
    }
    exit 1
}
Write-Host "✓ Configuration found" -ForegroundColor Green

# Build Docker images
Write-Host "`n[3/4] Building Docker images..." -ForegroundColor Yellow
Write-Host "This may take a few minutes on first run..." -ForegroundColor Cyan
docker-compose build
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Docker images built successfully" -ForegroundColor Green
}
else {
    Write-Host "✗ Error building Docker images" -ForegroundColor Red
    exit 1
}

# Start containers
Write-Host "`n[4/4] Starting containers..." -ForegroundColor Yellow
docker-compose up -d
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Containers started successfully" -ForegroundColor Green
}
else {
    Write-Host "✗ Error starting containers" -ForegroundColor Red
    exit 1
}

# Wait for services to be ready
Write-Host "`nWaiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "`n=================================================================" -ForegroundColor Cyan
Write-Host "✓ Application is running!" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend:        http://localhost" -ForegroundColor Green
Write-Host "Backend API:     http://localhost:8000" -ForegroundColor Green
Write-Host "API Docs:        http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Useful Commands:" -ForegroundColor Yellow
Write-Host "  Stop:          docker-compose down" -ForegroundColor Cyan
Write-Host "  View logs:     docker-compose logs -f" -ForegroundColor Cyan
Write-Host "  Rebuild:       docker-compose up -d --build" -ForegroundColor Cyan
Write-Host "  Restart:       docker-compose restart" -ForegroundColor Cyan
Write-Host ""
Write-Host "=================================================================" -ForegroundColor Cyan
