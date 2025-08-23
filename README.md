# TaskFlow - Advanced Data Structures & Algorithms Project

A comprehensive task management system demonstrating advanced data structures, algorithms, and software architecture patterns. Built as an educational project showcasing real-world applications of computer science concepts.

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip3 install flask flask-cors requests
   ```

2. **Run TaskFlow**
   ```bash
   python3 main.py
   ```
   This single command starts both backend and frontend services automatically.

3. **Access the Application**
   - The application will automatically open in your browser
   - Frontend: http://localhost:8080/landing/html/index.html
   - Backend API: http://localhost:5000
   - Technical Documentation: http://localhost:8080/info/html/info.html

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

## 🎯 Core Data Structures & Algorithms

### Data Structures Implemented
- **Hash Table (Dictionary)**: O(1) task lookup, insertion, deletion
- **Tree Structure**: Hierarchical task organization with parent-child relationships
- **Queue (FIFO)**: Task processing pipeline for background operations
- **Stack (LIFO)**: Undo/redo functionality and operation history
- **JSON Storage**: Persistent file-based storage with atomic operations

### Algorithms Demonstrated
- **Depth-First Search (DFS)**: Tree traversal, recursive deletion, hierarchy display
- **Breadth-First Search (BFS)**: Level-order processing, tree depth calculation
- **Atomic File Operations**: ACID-compliant data persistence
- **Topological Sorting**: Task dependency resolution (future enhancement)

## ✨ Features

### Frontend Architecture
- **Service-Based Design**: Unified launcher managing both frontend and backend
- **Absolute Path Routing**: Reliable navigation between all pages
- **Component Separation**: Each page in its own organized folder structure
- **Modern UI/UX**: Glass morphism effects, smooth animations, responsive design

### Task Management
- **Hierarchical Organization**: Unlimited nesting of tasks and subtasks
- **Smart Task Creation**: Plus buttons on cards for direct child task creation
- **Completion Tracking**: Visual strikethrough and statistics for completed tasks
- **ID Management**: Hidden task IDs with toggle buttons and hover tooltips
- **Modal Interface**: Clean overlay for task creation and editing

### Backend Services
- **JSON Storage Service**: Persistent storage with hash table optimization
- **RESTful API**: Complete CRUD operations with proper HTTP status codes
- **Background Processing**: Multi-threaded task processing pipeline
- **Statistics Engine**: Real-time analytics and performance metrics
- **Atomic Operations**: Data integrity with crash-safe file operations

## 🎯 Usage

1. **Start the Application**: Run `python3 main.py`
2. **Create Tasks**: Click "Add Task" button to open modal
3. **Organize Tasks**: Create hierarchical task structures
4. **Manage Tasks**: Edit, delete, and organize your tasks
5. **Navigate**: Use expand/collapse controls for better organization

## 🏗️ Technical Architecture

### Performance Characteristics
| Operation | Time Complexity | Space Complexity | Implementation |
|-----------|----------------|------------------|----------------|
| Add Task | O(1) | O(1) | Hash table insertion |
| Find Task | O(1) | O(1) | Hash table lookup |
| Delete Task | O(k) | O(h) | DFS traversal (k=subtasks, h=height) |
| Get All Tasks | O(n) | O(h) | Tree traversal |

### Storage Implementation
- **JSON-Based Persistence**: Human-readable, crash-safe storage
- **Atomic Write Operations**: Prevents data corruption
- **Hash Table Indexing**: O(1) lookup performance
- **Tree Structure**: Efficient hierarchical relationships

### Service Architecture
- **Unified Launcher**: Single command starts both services
- **Process Management**: Automatic cleanup and error handling
- **Browser Integration**: Automatic application launch

## 🚀 Advanced Project Ideas

### Data Structure Enhancements
- **B+ Tree Storage**: Handle millions of tasks efficiently
- **Bloom Filters**: Probabilistic duplicate detection
- **LRU Cache**: Frequently accessed task caching
- **Trie Structure**: Fast autocomplete and search

### Algorithm Implementations
- **Priority Queues**: Task scheduling by urgency
- **Graph Algorithms**: Complex dependency management
- **A* Pathfinding**: Optimal task completion ordering
- **Machine Learning**: Task completion time prediction

## 📚 Educational Value

This project demonstrates:
- **Real-world application** of CS concepts
- **Performance optimization** through data structure selection
- **Software architecture** patterns and best practices
- **Full-stack development** with modern technologies

## 🔧 Development

### Project Structure
```
todo_project/
├── main.py                    # Unified service launcher
├── backend/core/              # Core algorithms & data structures
│   ├── json_storage.py       # Persistent storage service
│   ├── task_node.py          # Task data structure
│   ├── task_queue.py         # FIFO processing queue
│   └── task_stack.py         # LIFO operation stack
├── frontend/                 # Organized page components
└── data/                     # Persistent storage location
```

### Key Features
- **Atomic Operations**: Crash-safe file writes
- **Service Management**: Automatic process lifecycle
- **Performance Monitoring**: Built-in statistics
- **Comprehensive Documentation**: Technical details with examples
