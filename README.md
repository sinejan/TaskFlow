# TaskFlow - Modern Task Management

A modern, hierarchical task management application with a clean, organized structure.

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip3 install flask flask-cors requests
   ```

2. **Run TaskFlow**
   ```bash
   python3 main.py
   ```

3. **Access the Application**
   - The application will automatically open in your browser
   - Frontend: http://localhost:8080/landing/html/index.html
   - Backend API: http://localhost:5000

## 📁 Project Structure

```
todo_project/
├── main.py                    # Unified launcher (starts both backend & frontend)
├── backend/                   # Backend server
│   ├── app.py                # Flask application
│   └── core/                 # Core business logic
├── frontend/                 # Frontend application
│   ├── landing/              # Landing page
│   │   ├── html/
│   │   ├── css/
│   │   └── js/
│   ├── task-manager/         # Main task management interface
│   │   ├── html/
│   │   ├── css/
│   │   └── js/
│   └── info/                 # System information page
│       ├── html/
│       ├── css/
│       └── js/
├── data/                     # Data storage
├── utils/                    # Utility functions
└── requirements.txt          # Python dependencies
```

## ✨ Features

### Landing Page
- Clean, modern design with two main options
- Removed backend server status message
- Simplified navigation

### Task Manager
- **Hidden Task IDs**: Click the `#` button to show/hide task IDs
- **Modal Interface**: Add new tasks via modal overlay
- **Collapsible Hierarchy**: Expand/collapse task trees
- **Global Controls**: Expand all / Collapse all buttons
- **Dark/Light Theme**: Toggle between themes
- **Invisible Scrollbars**: Clean UI without visible scrollbars
- **Responsive Design**: Works on all screen sizes

### Backend
- **In-Memory Storage**: Fast, lightweight task storage
- **RESTful API**: Full CRUD operations for tasks
- **Hierarchical Tasks**: Support for parent-child relationships
- **Real-time Processing**: Background task processing threads

## 🎯 Usage

1. **Start the Application**: Run `python3 main.py`
2. **Create Tasks**: Click "Add Task" button to open modal
3. **Organize Tasks**: Create hierarchical task structures
4. **Manage Tasks**: Edit, delete, and organize your tasks
5. **Navigate**: Use expand/collapse controls for better organization

## 🛠 Technical Details

- **Backend**: Flask with CORS support
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Storage**: In-memory (TaskTree data structure)
- **Architecture**: Separated frontend and backend with unified launcher
- **Styling**: Modern CSS with CSS variables for theming

## 🔧 Development

The project is now organized with clear separation of concerns:
- Each page has its own folder with HTML, CSS, and JS files
- Unified launcher handles both backend and frontend servers
- Clean project structure for easy maintenance and development

## 📝 Notes

- Backend uses in-memory storage (data is lost on restart)
- Frontend serves static files via Python's built-in HTTP server
- All dependencies are managed via requirements.txt
- The application automatically opens in your default browser
