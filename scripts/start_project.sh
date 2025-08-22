#!/bin/bash

echo "🚀 Starting Todo Project..."

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Start backend
echo "🔧 Starting backend server..."
cd backend
python app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Open frontend in browser
echo "🌐 Opening interface selector in browser..."
cd ..
open frontend/index.html

echo "✅ Project started successfully!"
echo "📍 Backend running at: http://localhost:5000"
echo "📍 Frontend opened in browser"
echo ""
echo "To stop the backend, press Ctrl+C or run: kill $BACKEND_PID"
echo "Backend PID: $BACKEND_PID"

# Keep script running to maintain backend
wait $BACKEND_PID
