# Smart E-Learning Automator - Start Both Servers
# This script starts both the backend API server and frontend React app

Write-Host "🎓 Smart E-Learning Automator - Full Stack Startup" -ForegroundColor Cyan
Write-Host "=" * 60

# Check if we're in the right directory
$currentDir = Get-Location
if (-not (Test-Path "backend" -PathType Container) -or -not (Test-Path "frontend" -PathType Container)) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    Write-Host "Expected structure:" -ForegroundColor Yellow
    Write-Host "  - backend/"
    Write-Host "  - frontend/"
    exit 1
}

# Function to start backend
function Start-Backend {
    Write-Host "`n🔧 Starting Backend API Server..." -ForegroundColor Green
    Write-Host "📡 API will be available at: http://localhost:8000" -ForegroundColor Yellow
    Write-Host "📊 API Documentation: http://localhost:8000/docs" -ForegroundColor Yellow
    Write-Host "🔌 WebSocket: ws://localhost:8000/ws" -ForegroundColor Yellow
    
    # Activate virtual environment and start server
    Set-Location "backend"
    if (Test-Path "../.venv/Scripts/Activate.ps1") {
        & "../.venv/Scripts/Activate.ps1"
        python start_server.py
    } else {
        Write-Host "⚠️  Virtual environment not found. Install dependencies first:" -ForegroundColor Yellow
        Write-Host "  pip install fastapi uvicorn selenium webdriver-manager requests beautifulsoup4" -ForegroundColor Gray
        python start_server.py
    }
}

# Function to start frontend
function Start-Frontend {
    Write-Host "`n⚛️  Starting Frontend React App..." -ForegroundColor Blue
    Write-Host "🌐 Frontend will be available at: http://localhost:3000" -ForegroundColor Yellow
    
    Set-Location "../frontend"
    if (Test-Path "node_modules") {
        npm start
    } else {
        Write-Host "⚠️  Node modules not found. Installing dependencies..." -ForegroundColor Yellow
        npm install
        npm start
    }
}

# Ask user what to start
Write-Host "`nWhat would you like to start?" -ForegroundColor White
Write-Host "1. Backend Only (API Server)" -ForegroundColor Gray
Write-Host "2. Frontend Only (React App)" -ForegroundColor Gray  
Write-Host "3. Both (Recommended)" -ForegroundColor Green
Write-Host "4. Exit" -ForegroundColor Gray

$choice = Read-Host "`nEnter your choice (1-4)"

switch ($choice) {
    "1" {
        Start-Backend
    }
    "2" {
        Start-Frontend  
    }
    "3" {
        Write-Host "`n🚀 Starting both servers..." -ForegroundColor Cyan
        Write-Host "💡 Backend will start in this terminal, Frontend will open in a new window" -ForegroundColor Yellow
        
        # Start frontend in new terminal
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$currentDir'; Write-Host '⚛️  Starting Frontend...' -ForegroundColor Blue; cd frontend; npm start"
        
        # Start backend in current terminal
        Start-Sleep 2
        Start-Backend
    }
    "4" {
        Write-Host "👋 Goodbye!" -ForegroundColor Cyan
        exit 0
    }
    default {
        Write-Host "❌ Invalid choice. Please run the script again." -ForegroundColor Red
        exit 1
    }
}