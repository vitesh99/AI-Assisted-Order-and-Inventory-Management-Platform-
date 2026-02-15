# Script to start backend services individually in new terminals
# Prerequisites: Python installed, venv created, dependencies installed in each service

# 1. Start Database (using Docker for convenience because installing Postgres locally is harder)
Write-Host "Starting Database..."
docker start ai_inventory_db
if ($?) {
    Write-Host "Database started."
} else {
    Write-Host "Docker container ai_inventory_db not found or failed to start. Trying to run a new one..."
    docker run -d --name ai_inventory_db -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=ai_inventory_auth -v postgres_data:/var/lib/postgresql/data postgres:15-alpine
}

# Wait for DB
Start-Sleep -Seconds 5

# Function to start a service in a new Python process
function Start-Service {
    param (
        [string]$ServiceName,
        [string]$Path,
        [int]$Port
    )
    Write-Host "Starting $ServiceName on port $Port..."
    
    # Check if venv exists in the root or service folder
    $VenvPath = "venv\Scripts\activate.ps1"
    if (-not (Test-Path $VenvPath)) {
        $VenvPath = "..\venv\Scripts\activate.ps1"
    }
    
    # Command to run in new window
    # We assume requirements are installed. If not, user should run 'pip install -r requirements.txt' in each folder.
    # But for now, we assume global venv or service-specific venv.
    # Let's assume the user is using the root venv.
    
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '$VenvPath'; cd '$Path'; uvicorn app.main:app --host 0.0.0.0 --port $Port --reload"
}

# 2. Start Auth Service
Start-Service -ServiceName "Auth Service" -Path "auth-service" -Port 8001

# 3. Start Inventory Service
Start-Service -ServiceName "Inventory Service" -Path "inventory-service" -Port 8002

# 4. Start Order Service
Start-Service -ServiceName "Order Service" -Path "order-service" -Port 8003

# 5. Start Gateway Service
Start-Service -ServiceName "Gateway Service" -Path "gateway-service" -Port 8000

Write-Host "All services launching in separate windows."
Write-Host "Gateway: http://localhost:8000"
Write-Host "Auth: http://localhost:8001"
Write-Host "Inventory: http://localhost:8002"
Write-Host "Order: http://localhost:8003"
