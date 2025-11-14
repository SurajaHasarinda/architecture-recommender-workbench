#!/bin/bash
# Bash script to start the application with Docker

echo "================================================================="
echo "     Architecture Recommendation Agent - Docker Setup          "
echo "================================================================="
echo ""

# Check Docker
echo "[1/4] Checking Docker installation..."
if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null; then
    echo "✗ Docker or Docker Compose not found!"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi
echo "✓ Docker found"

# Check .env
echo ""
echo "[2/4] Checking configuration..."
if [ ! -f ".env" ]; then
    echo "✗ .env file not found!"
    if [ -f ".env.example" ]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo "Please edit .env and add your GOOGLE_API_KEY"
    fi
    exit 1
fi
echo "✓ Configuration found"

# Build images
echo ""
echo "[3/4] Building Docker images..."
echo "This may take a few minutes on first run..."
docker-compose build
if [ $? -eq 0 ]; then
    echo "✓ Images built"
else
    echo "✗ Error building images"
    exit 1
fi

# Start containers
echo ""
echo "[4/4] Starting containers..."
docker-compose up -d
if [ $? -eq 0 ]; then
    echo "✓ Containers started"
else
    echo "✗ Error starting containers"
    exit 1
fi

# Wait for services
echo ""
echo "Waiting for services to start..."
sleep 5

echo ""
echo "================================================================="
echo "✓ Application is running!"
echo ""
echo "Frontend:        http://localhost"
echo "Backend API:     http://localhost:8000"
echo "API Docs:        http://localhost:8000/docs"
echo ""
echo "Useful Commands:"
echo "  Stop:          docker-compose down"
echo "  View logs:     docker-compose logs -f"
echo "  Rebuild:       docker-compose up -d --build"
echo "  Restart:       docker-compose restart"
echo ""
echo "================================================================="
