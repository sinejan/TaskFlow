# TaskFlow - Modern Todo Project

A full-stack todo application with Flask backend and multiple frontend options.

## ✨ Features

### Core Functionality
- ✅ Add new tasks with name and description
- 📋 View all tasks in a hierarchical structure
- 🔗 Support for parent-child task relationships
- 🔄 Real-time task processing with queue and stack
- ⏰ Alarm system for task due dates (email notifications)

### Modern Frontend Features
- 🎨 Beautiful gradient design with smooth animations
- 📊 Real-time task statistics dashboard
- 🌳 Hierarchical task visualization with indentation
- 📋 Click-to-copy task IDs
- ⚡ Quick subtask creation buttons
- 🔄 Auto-refresh every 30 seconds
- 📱 Fully responsive design
- 🎯 Enhanced user experience with notifications

## Project Structure

```
todo_project/
├── run_taskflow.sh         # 🚀 ONE-CLICK STARTUP SCRIPT
├── backend/                # Backend API and core logic
│   ├── app.py             # Flask API server
│   └── core/              # Core task management modules
├── frontend/              # Frontend interfaces
│   ├── index.html         # Interface selection page
│   ├── frontend.html      # Simple web interface
│   ├── frontend_fancy.html # Modern web interface (⭐ Recommended)
│   └── info.html          # System architecture documentation
├── docs/                  # Documentation
│   ├── README.md          # This file
│   └── PROJECT_STRUCTURE.md # Detailed project structure
├── scripts/               # Utility scripts
├── static/                # Static assets (future use)
├── requirements.txt       # Python dependencies
└── venv/                  # Virtual environment
```

## 🚀 Quick Start

### One-Click Startup (Recommended)
```bash
./run_taskflow.sh
```

### Alternative Methods

1. **Using the startup script:**
   ```bash
   ./scripts/start_project.sh
   ```

2. **Manual start:**
   ```bash
   # Activate virtual environment
   source venv/bin/activate

   # Start backend
   cd backend && python app.py

   # Open frontend/index.html in your browser
   ```

## API Endpoints

- `GET /` - Health check
- `POST /add_task` - Add a new task
  ```json
  {
    "name": "Task name",
    "description": "Task description",
    "parent_id": "optional-parent-id"
  }
  ```
- `GET /get_tasks` - Get all tasks

## Frontend Options

### 🚀 Modern Interface (Recommended)
- **File**: `frontend_fancy.html`
- **Features**: Beautiful design, animations, hierarchical view, statistics
- **Best for**: Enhanced user experience and visual appeal

### 📝 Simple Interface
- **File**: `frontend.html`
- **Features**: Clean, minimal design focused on functionality
- **Best for**: Quick task management without distractions

### 🎯 Interface Selector
- **File**: `index.html`
- **Purpose**: Choose between modern and simple interfaces

## Usage

### Modern Interface
1. Open `frontend_fancy.html` or use the startup script
2. View real-time statistics at the top
3. Fill in the task form with name and description
4. Optionally specify a parent task ID for hierarchical tasks
5. Click "Add Task" to create the task
6. Tasks appear in hierarchical view with indentation
7. Click task IDs to copy them
8. Use "Add Subtask" buttons for quick parent ID setting

### Simple Interface
1. Open `frontend.html` in your browser
2. Fill in the task form with name and description
3. Optionally specify a parent task ID for hierarchical tasks
4. Click "Ekle" (Add) to create the task
5. Tasks will appear in the list above the form

## Technical Details

- **Backend**: Flask with CORS enabled
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Task Processing**: Queue → Stack → Processed list
- **Threading**: Separate threads for listening and sending
- **Alarm System**: Email notifications for due dates

## Dependencies

- Flask 2.3.3
- Flask-CORS 4.0.0

## Notes

- The backend runs on `http://localhost:5000`
- The frontend communicates with the backend via CORS-enabled API calls
- Email credentials in `alarm_thread.py` should be configured for notifications
