from flask import Flask, request, jsonify
from flask_cors import CORS
from core.task_node import TaskNode
from core.json_storage import JSONStorage
from core.task_queue import TaskQueue
from core.task_stack import TaskStack
from core.thread_worker import ListenerThread, SenderThread
from core.alarm_thread import AlarmThread


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize JSON storage service
storage = JSONStorage()

# Initialize data structures for processing
queue = TaskQueue()
stack = TaskStack()
processed_tasks = []

# Thread'leri başlat
listener = ListenerThread(queue, stack)
sender = SenderThread(stack, processed_tasks)

listener.start()
sender.start()

@app.route('/')
def index():
    return jsonify({"message": "Backend API is running..use /add_task to add a task."})

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    parent_id = data.get("parent_id", None)

    if not name or not description:
        return jsonify({"error": "Name and description required"}), 400

    new_task = TaskNode(name, description, parent_id=parent_id)
    success = storage.add_task(new_task, parent_id)

    if success:
        queue.enqueue(new_task)
        return jsonify({
            "message": "Task added successfully.",
            "task_id": new_task.id
        }), 200
    else:
        return jsonify({"error": "Failed to add task"}), 500

@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    all_tasks = storage.get_all_tasks()
    return jsonify(all_tasks), 200

@app.route('/update_task/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    name = data.get("name")
    description = data.get("description")

    if not name or not description:
        return jsonify({"error": "Name and description required"}), 400

    # Update task in storage
    updates = {"name": name, "description": description}
    success = storage.update_task(task_id, updates)

    if not success:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "message": "Task updated successfully.",
        "task_id": task_id
    }), 200

@app.route('/delete_task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Delete task from storage
    success = storage.delete_task(task_id)
    if not success:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "message": "Task deleted successfully.",
        "task_id": task_id
    }), 200

@app.route('/toggle_task_completion/<task_id>', methods=['PUT'])
def toggle_task_completion(task_id):
    # Get current task
    task = storage.get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Toggle completion status
    new_completed = not task.get("completed", False)
    success = storage.update_task(task_id, {"completed": new_completed})

    if not success:
        return jsonify({"error": "Failed to update task"}), 500

    return jsonify({
        "message": "Task completion status updated.",
        "task_id": task_id,
        "completed": new_completed
    }), 200

@app.route('/statistics', methods=['GET'])
def get_statistics():
    stats = storage.get_statistics()
    return jsonify(stats), 200

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No Content

if __name__ == '__main__':
    print("✅ Backend API is running on port 5000. Access it here: http://localhost:5000")
    app.run(debug=True)

alarm_thread = AlarmThread(storage, check_interval=30, alarm_before=60)
alarm_thread.start()