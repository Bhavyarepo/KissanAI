#!/bin/bash

# AI Crop Recommendation System Startup Script

echo "🌱 Starting AI Crop Recommendation System..."

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "🐳 Docker found. Starting with Docker Compose..."
    
    # Check if docker-compose is installed
    if command -v docker-compose &> /dev/null; then
        docker-compose up -d
        echo "✅ Application started successfully!"
        echo "🌐 Frontend: http://localhost:3000"
        echo "🔧 Backend API: http://localhost:8000"
        echo "📚 API Docs: http://localhost:8000/docs"
    else
        echo "❌ docker-compose not found. Please install docker-compose."
        exit 1
    fi
else
    echo "🐍 Docker not found. Starting with local development..."
    
    # Check if Python is installed
    if command -v python3 &> /dev/null; then
        echo "📦 Installing Python dependencies..."
        pip install -r requirements.txt
        
        echo "🚀 Starting backend server..."
        cd backend
        python run.py &
        BACKEND_PID=$!
        
        # Wait a moment for backend to start
        sleep 5
        
        # Check if Node.js is installed
        if command -v node &> /dev/null; then
            echo "📦 Installing Node.js dependencies..."
            cd ../frontend
            npm install
            
            echo "🚀 Starting frontend server..."
            npm run dev &
            FRONTEND_PID=$!
            
            echo "✅ Application started successfully!"
            echo "🌐 Frontend: http://localhost:3000"
            echo "🔧 Backend API: http://localhost:8000"
            echo "📚 API Docs: http://localhost:8000/docs"
            
            # Wait for user to stop the application
            echo "Press Ctrl+C to stop the application"
            wait
        else
            echo "❌ Node.js not found. Please install Node.js 18+ to run the frontend."
            kill $BACKEND_PID
            exit 1
        fi
    else
        echo "❌ Python not found. Please install Python 3.11+ to run the backend."
        exit 1
    fi
fi





