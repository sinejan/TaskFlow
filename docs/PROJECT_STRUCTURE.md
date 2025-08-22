# TaskFlow - Project Structure

## 📁 Directory Organization

```
todo_project/
├── 🚀 run_taskflow.sh          # Main startup script (ONE-CLICK START)
├── 📋 requirements.txt         # Python dependencies
├── 🐍 main.py                  # Standalone test script
├── 🧪 test_core.py            # Core functionality tests
│
├── 📂 backend/                 # Backend API and core logic
│   ├── 🌐 app.py              # Flask API server
│   └── 📂 core/               # Core business logic modules
│       ├── 📄 __init__.py
│       ├── 🔧 task_node.py     # Task data structure
│       ├── 🌳 task_tree.py     # Hierarchical task management
│       ├── 📥 task_queue.py    # FIFO task queue
│       ├── 📤 task_stack.py    # LIFO task stack
│       ├── 🧵 thread_worker.py # Background processing threads
│       ├── ⏰ alarm_thread.py  # Email notification system
│       ├── 📅 due_date_checker.py # Date validation
│       └── 🔍 search.py        # Task search functionality
│
├── 📂 frontend/               # Frontend interfaces
│   ├── 🏠 index.html         # Interface selector page
│   ├── ✨ frontend_fancy.html # Modern interface (RECOMMENDED)
│   ├── 📝 frontend.html      # Simple interface
│   └── 📚 info.html          # System architecture documentation
│
├── 📂 static/                 # Static assets (future use)
│   ├── 📂 css/               # Stylesheets
│   ├── 📂 js/                # JavaScript modules
│   └── 📂 assets/            # Images, icons, etc.
│
├── 📂 scripts/               # Utility scripts
│   └── 🔧 start_project.sh   # Legacy startup script
│
├── 📂 docs/                  # Documentation
│   ├── 📖 README.md          # Main documentation
│   └── 📋 PROJECT_STRUCTURE.md # This file
│
├── 📂 data/                  # Data files
│   └── 📊 sample_data.json   # Sample task data
│
├── 📂 utils/                 # Utility modules
│   ├── 📧 mail_sender.py     # Email utilities
│   └── ⏱️ time_utils.py      # Time/date utilities
│
└── 📂 venv/                  # Python virtual environment
    ├── 📂 bin/
    ├── 📂 lib/
    └── 📄 pyvenv.cfg
```

## 🚀 Quick Start

### One-Click Startup
```bash
./run_taskflow.sh
```

This script will:
1. ✅ Check/create virtual environment
2. ✅ Install dependencies
3. ✅ Start backend server
4. ✅ Open frontend in browser
5. ✅ Provide status monitoring

### Manual Startup
```bash
# Activate virtual environment
source venv/bin/activate

# Start backend
cd backend && python app.py

# Open frontend/index.html in browser
```

## 🏗️ Architecture Layers

### 1. **Presentation Layer** (`frontend/`)
- **Interface Selector** (`index.html`) - Choose between interfaces
- **Modern Interface** (`frontend_fancy.html`) - Feature-rich UI
- **Simple Interface** (`frontend.html`) - Minimal UI
- **Documentation** (`info.html`) - System architecture guide

### 2. **API Layer** (`backend/app.py`)
- RESTful endpoints
- CORS enabled
- Request validation
- Response formatting

### 3. **Business Logic Layer** (`backend/core/`)
- Task management
- Data structures
- Processing algorithms
- Background threads

### 4. **Data Layer**
- In-memory storage (current)
- Task tree structure
- Queue/Stack processing

## 🔧 Core Components

### Backend Modules

| Module | Purpose | Key Features |
|--------|---------|--------------|
| `task_node.py` | Task data structure | UUID generation, serialization |
| `task_tree.py` | Hierarchical organization | Parent-child relationships, traversal |
| `task_queue.py` | FIFO processing | Thread-safe queue operations |
| `task_stack.py` | LIFO processing | Stack-based task execution |
| `thread_worker.py` | Background processing | Listener/Sender threads |
| `alarm_thread.py` | Notifications | Email alerts for due dates |

### Frontend Features

| Interface | Target User | Key Features |
|-----------|-------------|--------------|
| Modern | Power users | Animations, dark mode, CRUD, statistics |
| Simple | Basic users | Clean design, essential features only |

## 🌐 API Endpoints

```
GET  /              # Health check
POST /add_task      # Create new task
GET  /get_tasks     # Retrieve all tasks
```

### Request/Response Format

**Add Task:**
```json
POST /add_task
{
  "name": "Task Name",
  "description": "Task Description",
  "parent_id": "optional-parent-uuid"
}
```

**Get Tasks:**
```json
GET /get_tasks
[
  {
    "id": "uuid-string",
    "name": "Task Name",
    "description": "Task Description",
    "due_date": null,
    "children": ["child-uuid-1", "child-uuid-2"]
  }
]
```

## 🔄 Data Flow

1. **User Input** → Frontend form
2. **API Call** → Flask endpoint
3. **Validation** → Request processing
4. **Storage** → Task tree + Queue
5. **Processing** → Background threads
6. **Response** → JSON data
7. **UI Update** → Frontend rendering

## 🧵 Threading Model

- **Main Thread** - Flask API server
- **Listener Thread** - Queue → Stack (1s intervals)
- **Sender Thread** - Stack → Processed (2s intervals)  
- **Alarm Thread** - Due date monitoring (30s intervals)

## 📱 Frontend Architecture

### Modern Interface Features
- 🎨 CSS Grid/Flexbox layout
- 🌙 Dark/Light theme toggle
- 📊 Real-time statistics
- 🔄 Auto-refresh (30s)
- ✨ Smooth animations
- 📱 Responsive design
- 🎯 CRUD operations
- 📋 Hierarchical display

### Technology Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python Flask, Threading
- **Styling**: CSS Custom Properties, Flexbox, Grid
- **Icons**: Font Awesome 6
- **Fonts**: Inter (Google Fonts)

## 🔧 Development

### Adding New Features
1. Backend: Add endpoint in `app.py`
2. Core Logic: Implement in `backend/core/`
3. Frontend: Update UI in `frontend/`
4. Documentation: Update relevant docs

### Testing
```bash
python test_core.py  # Core functionality
python main.py       # Standalone test
```

## 📝 Configuration

### Environment Variables
- Backend runs on `localhost:5000`
- Frontend uses relative paths
- CORS enabled for all origins

### Customization
- Modify CSS variables in frontend files
- Adjust thread intervals in core modules
- Configure email settings in `alarm_thread.py`

## 🚀 Deployment Notes

- Current setup is for development
- For production: Use WSGI server (Gunicorn)
- Consider database integration
- Implement proper authentication
- Add environment-based configuration
