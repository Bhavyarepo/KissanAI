@echo off
echo 🌱 Starting AI Crop Recommendation System...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% == 0 (
    echo 🐳 Docker found. Starting with Docker Compose...
    
    REM Check if docker-compose is installed
    docker-compose --version >nul 2>&1
    if %errorlevel% == 0 (
        docker-compose up -d
        echo ✅ Application started successfully!
        echo 🌐 Frontend: http://localhost:3000
        echo 🔧 Backend API: http://localhost:8000
        echo 📚 API Docs: http://localhost:8000/docs
        pause
    ) else (
        echo ❌ docker-compose not found. Please install docker-compose.
        pause
        exit /b 1
    )
) else (
    echo 🐍 Docker not found. Starting with local development...
    
    REM Check if Python is installed
    python --version >nul 2>&1
    if %errorlevel% == 0 (
        echo 📦 Installing Python dependencies...
        pip install -r requirements.txt
        
        echo 🚀 Starting backend server...
        cd backend
        start "Backend Server" python run.py
        
        REM Wait a moment for backend to start
        timeout /t 5 /nobreak >nul
        
        REM Check if Node.js is installed
        node --version >nul 2>&1
        if %errorlevel% == 0 (
            echo 📦 Installing Node.js dependencies...
            cd ..\frontend
            call npm install
            
            echo 🚀 Starting frontend server...
            start "Frontend Server" npm run dev
            
            echo ✅ Application started successfully!
            echo 🌐 Frontend: http://localhost:3000
            echo 🔧 Backend API: http://localhost:8000
            echo 📚 API Docs: http://localhost:8000/docs
            echo Press any key to stop the application
            pause >nul
        ) else (
            echo ❌ Node.js not found. Please install Node.js 18+ to run the frontend.
            pause
            exit /b 1
        )
    ) else (
        echo ❌ Python not found. Please install Python 3.11+ to run the backend.
        pause
        exit /b 1
    )
)





