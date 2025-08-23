// Task Manager JavaScript
class TaskManager {
    constructor() {
        this.tasks = [];
        this.expandedTasks = new Set();
        this.currentEditingTask = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadTasks();
        this.setupTheme();
    }

    bindEvents() {
        // Theme toggle
        document.getElementById('theme-toggle').addEventListener('click', () => this.toggleTheme());
        
        // Refresh button
        document.getElementById('refresh-btn').addEventListener('click', () => this.loadTasks());
        
        // Add task modal
        document.getElementById('add-task-btn').addEventListener('click', () => this.showAddTaskModal());
        document.getElementById('modal-close').addEventListener('click', () => this.hideAddTaskModal());
        document.getElementById('cancel-btn').addEventListener('click', () => this.hideAddTaskModal());
        
        // Edit task modal
        document.getElementById('edit-modal-close').addEventListener('click', () => this.hideEditTaskModal());
        document.getElementById('edit-cancel-btn').addEventListener('click', () => this.hideEditTaskModal());
        
        // Forms
        document.getElementById('add-task-form').addEventListener('submit', (e) => this.handleAddTask(e));
        document.getElementById('edit-task-form').addEventListener('submit', (e) => this.handleEditTask(e));
        
        // Expand/Collapse all
        document.getElementById('expand-all-btn').addEventListener('click', () => this.expandAll());
        document.getElementById('collapse-all-btn').addEventListener('click', () => this.collapseAll());
        
        // Modal backdrop click
        document.getElementById('add-task-modal').addEventListener('click', (e) => {
            if (e.target.id === 'add-task-modal') this.hideAddTaskModal();
        });
        document.getElementById('edit-task-modal').addEventListener('click', (e) => {
            if (e.target.id === 'edit-task-modal') this.hideEditTaskModal();
        });
    }

    async loadTasks() {
        try {
            const response = await fetch('http://localhost:5000/get_tasks');
            if (response.ok) {
                this.tasks = await response.json();
                this.renderTasks();
                this.updateStats();
                this.updateParentTaskOptions();
            } else {
                this.showError('Failed to load tasks');
            }
        } catch (error) {
            this.showError('Error connecting to server');
            console.error('Error:', error);
        }
    }

    renderTasks() {
        const container = document.getElementById('tasks-container');
        container.innerHTML = '';

        if (this.tasks.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
                    <i class="fas fa-tasks" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                    <p>No tasks yet. Click "Add Task" to get started!</p>
                </div>
            `;
            return;
        }

        // Render all tasks in flat structure with hierarchy levels
        this.renderTasksFlat(container);
    }

    renderTasksFlat(container) {
        // Start with root tasks
        const rootTasks = this.tasks.filter(task => !task.parent_id);

        rootTasks.forEach(task => {
            this.renderTaskWithChildren(container, task, 0);
        });
    }

    renderTaskWithChildren(container, task, level) {
        // Only render if task should be visible (expanded or root)
        if (level === 0 || this.isTaskVisible(task)) {
            const taskElement = this.createTaskElement(task, level);
            container.appendChild(taskElement);
        }

        // Render children if parent is expanded
        if (this.expandedTasks.has(task.id)) {
            const children = this.getChildTasks(task.id);
            children.forEach(childTask => {
                this.renderTaskWithChildren(container, childTask, level + 1);
            });
        }
    }

    isTaskVisible(task) {
        // Check if all parent tasks are expanded
        let currentTask = task;
        while (currentTask.parent_id) {
            const parent = this.tasks.find(t => t.id === currentTask.parent_id);
            if (!parent || !this.expandedTasks.has(parent.id)) {
                return false;
            }
            currentTask = parent;
        }
        return true;
    }

    createTaskElement(task, level = 0) {
        const taskDiv = document.createElement('div');
        taskDiv.className = 'task-card';
        taskDiv.dataset.taskId = task.id;

        // Set hierarchy level for styling
        if (level > 0) {
            taskDiv.dataset.level = Math.min(level, 5); // Max 5 levels for styling
        }

        const hasChildren = this.getChildTasks(task.id).length > 0;
        const isExpanded = this.expandedTasks.has(task.id);
        const completedClass = task.completed ? 'completed' : '';

        taskDiv.innerHTML = `
            <div class="task-header">
                <div class="task-info">
                    ${hasChildren ? `
                        <button class="task-expand-btn" onclick="taskManager.toggleTask('${task.id}')">
                            <i class="fas fa-chevron-${isExpanded ? 'down' : 'right'}"></i>
                        </button>
                    ` : '<div style="width: 24px;"></div>'}
                    <div class="task-content">
                        <div class="task-title ${completedClass}">${this.escapeHtml(task.name)}</div>
                        <div class="task-description ${completedClass}">${this.escapeHtml(task.description)}</div>
                    </div>
                </div>
                <div class="task-actions">
                    <button class="task-btn add-child-btn" onclick="taskManager.addChildTask('${task.id}')" title="Add child task">
                        <i class="fas fa-plus"></i>
                    </button>
                    <button class="task-btn complete-btn ${completedClass}" onclick="taskManager.toggleCompletion('${task.id}')" title="${task.completed ? 'Mark incomplete' : 'Mark complete'}">
                        <i class="fas fa-${task.completed ? 'undo' : 'check'}"></i>
                    </button>
                    <button class="task-id-btn" onclick="taskManager.toggleTaskId(this, '${task.id}')">
                        #
                        <div class="task-id-tooltip">${task.id}</div>
                    </button>
                    <button class="task-btn edit-btn" onclick="taskManager.editTask('${task.id}')" title="Edit task">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="task-btn delete-btn" onclick="taskManager.deleteTask('${task.id}')" title="Delete task">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;

        return taskDiv;
    }

    getChildTasks(parentId) {
        return this.tasks.filter(task => task.parent_id === parentId);
    }

    toggleTask(taskId) {
        if (this.expandedTasks.has(taskId)) {
            this.expandedTasks.delete(taskId);
        } else {
            this.expandedTasks.add(taskId);
        }
        this.renderTasks();
    }

    expandAll() {
        this.tasks.forEach(task => {
            if (this.getChildTasks(task.id).length > 0) {
                this.expandedTasks.add(task.id);
            }
        });
        this.renderTasks();
    }

    collapseAll() {
        this.expandedTasks.clear();
        this.renderTasks();
    }

    toggleTaskId(button, taskId) {
        const isShowing = button.textContent.trim() === taskId;
        if (isShowing) {
            button.innerHTML = `# <div class="task-id-tooltip">${taskId}</div>`;
        } else {
            button.innerHTML = taskId;
            // Copy to clipboard
            navigator.clipboard.writeText(taskId).then(() => {
                this.showSuccess('Task ID copied to clipboard!');
            });
        }
    }

    addChildTask(parentId) {
        this.showAddTaskModal();
        // Pre-select the parent task
        const parentSelect = document.getElementById('parent-task');
        parentSelect.value = parentId;
    }

    showAddTaskModal() {
        document.getElementById('add-task-modal').classList.add('show');
        document.getElementById('task-name').focus();
    }

    hideAddTaskModal() {
        document.getElementById('add-task-modal').classList.remove('show');
        document.getElementById('add-task-form').reset();
    }

    showEditTaskModal() {
        document.getElementById('edit-task-modal').classList.add('show');
        document.getElementById('edit-task-name').focus();
    }

    hideEditTaskModal() {
        document.getElementById('edit-task-modal').classList.remove('show');
        document.getElementById('edit-task-form').reset();
        this.currentEditingTask = null;
    }

    async handleAddTask(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const taskData = {
            name: formData.get('name'),
            description: formData.get('description'),
            parent_id: formData.get('parent_id') || null
        };

        try {
            const response = await fetch('http://localhost:5000/add_task', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(taskData)
            });

            if (response.ok) {
                this.hideAddTaskModal();
                this.loadTasks();
                this.showSuccess('Task added successfully!');
            } else {
                this.showError('Failed to add task');
            }
        } catch (error) {
            this.showError('Error connecting to server');
            console.error('Error:', error);
        }
    }

    editTask(taskId) {
        const task = this.tasks.find(t => t.id === taskId);
        if (!task) return;

        this.currentEditingTask = taskId;
        document.getElementById('edit-task-name').value = task.name;
        document.getElementById('edit-task-description').value = task.description;
        this.showEditTaskModal();
    }

    async handleEditTask(e) {
        e.preventDefault();
        if (!this.currentEditingTask) return;

        const formData = new FormData(e.target);
        const taskData = {
            name: formData.get('name'),
            description: formData.get('description')
        };

        try {
            const response = await fetch(`http://localhost:5000/update_task/${this.currentEditingTask}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(taskData)
            });

            if (response.ok) {
                this.hideEditTaskModal();
                this.loadTasks();
                this.showSuccess('Task updated successfully!');
            } else {
                this.showError('Failed to update task');
            }
        } catch (error) {
            this.showError('Error connecting to server');
            console.error('Error:', error);
        }
    }

    async toggleCompletion(taskId) {
        try {
            const response = await fetch(`http://localhost:5000/toggle_task_completion/${taskId}`, {
                method: 'PUT'
            });

            if (response.ok) {
                this.loadTasks();
                const result = await response.json();
                this.showSuccess(`Task marked as ${result.completed ? 'complete' : 'incomplete'}!`);
            } else {
                this.showError('Failed to update task completion');
            }
        } catch (error) {
            this.showError('Error connecting to server');
            console.error('Error:', error);
        }
    }

    async deleteTask(taskId) {
        if (!confirm('Are you sure you want to delete this task? This action cannot be undone.')) {
            return;
        }

        try {
            const response = await fetch(`http://localhost:5000/delete_task/${taskId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.loadTasks();
                this.showSuccess('Task deleted successfully!');
            } else {
                this.showError('Failed to delete task');
            }
        } catch (error) {
            this.showError('Error connecting to server');
            console.error('Error:', error);
        }
    }

    updateStats() {
        const totalTasks = this.tasks.length;
        const completedTasks = this.tasks.filter(task => task.completed).length;
        const pendingTasks = totalTasks - completedTasks;

        document.getElementById('total-tasks').textContent = totalTasks;
        document.getElementById('completed-tasks').textContent = completedTasks;
        document.getElementById('pending-tasks').textContent = pendingTasks;
    }

    updateParentTaskOptions() {
        const select = document.getElementById('parent-task');
        select.innerHTML = '<option value="">None (Root Task)</option>';
        
        this.tasks.forEach(task => {
            const option = document.createElement('option');
            option.value = task.id;
            option.textContent = task.name;
            select.appendChild(option);
        });
    }

    setupTheme() {
        const savedTheme = localStorage.getItem('taskflow-theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
        this.updateThemeIcon(savedTheme);
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('taskflow-theme', newTheme);
        this.updateThemeIcon(newTheme);
    }

    updateThemeIcon(theme) {
        const icon = document.querySelector('#theme-toggle i');
        icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showNotification(message, type) {
        // Simple notification system
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            animation: slideInRight 0.3s ease-out;
            background: ${type === 'success' ? '#10b981' : '#ef4444'};
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// Initialize the task manager
const taskManager = new TaskManager();

// Add CSS for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);
