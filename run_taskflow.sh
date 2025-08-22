#!/bin/bash

# TaskFlow - One-Click Startup Script
# This script starts the entire TaskFlow application

echo "🚀 Starting TaskFlow Application..."
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found!"
    print_step "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment"
        exit 1
    fi
    print_status "Virtual environment created successfully"
fi

# Activate virtual environment
print_step "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment"
    exit 1
fi
print_status "Virtual environment activated"

# Install dependencies
print_step "Installing/updating dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    print_warning "Some dependencies might have failed to install"
else
    print_status "Dependencies installed successfully"
fi

# Check if backend is already running
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    print_warning "Backend already running on port 5000"
    print_step "Stopping existing backend..."
    pkill -f "python.*app.py"
    sleep 2
fi

# Start backend server
print_step "Starting backend server..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
print_step "Waiting for backend to initialize..."
sleep 3

# Check if backend started successfully
if ps -p $BACKEND_PID > /dev/null; then
    print_status "Backend server started successfully (PID: $BACKEND_PID)"
else
    print_error "Failed to start backend server"
    exit 1
fi

# Test backend connection
print_step "Testing backend connection..."
if curl -s http://localhost:5000/ > /dev/null; then
    print_status "Backend is responding correctly"
else
    print_warning "Backend might not be fully ready yet"
fi

# Open frontend in browser
print_step "Opening TaskFlow interface..."
if command -v open >/dev/null 2>&1; then
    # macOS
    open frontend/index.html
elif command -v xdg-open >/dev/null 2>&1; then
    # Linux
    xdg-open frontend/index.html
elif command -v start >/dev/null 2>&1; then
    # Windows
    start frontend/index.html
else
    print_warning "Could not auto-open browser. Please manually open: frontend/index.html"
fi

echo ""
echo "🎉 TaskFlow is now running!"
echo "=================================="
print_status "Backend API: http://localhost:5000"
print_status "Frontend: Open frontend/index.html in your browser"
print_status "Documentation: Open frontend/info.html for system architecture"
echo ""
print_status "Backend PID: $BACKEND_PID"
echo ""
echo "To stop TaskFlow:"
echo "  - Press Ctrl+C in this terminal"
echo "  - Or run: kill $BACKEND_PID"
echo ""
echo "Logs will appear below..."
echo "=================================="

# Function to cleanup on exit
cleanup() {
    echo ""
    print_step "Shutting down TaskFlow..."
    if ps -p $BACKEND_PID > /dev/null; then
        kill $BACKEND_PID
        print_status "Backend server stopped"
    fi
    print_status "TaskFlow shutdown complete"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Keep script running and show backend logs
wait $BACKEND_PID
