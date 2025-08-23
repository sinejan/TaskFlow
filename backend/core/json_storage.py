"""
JSON Storage Service for TaskFlow
Provides persistent storage using JSON files with efficient data structures
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from .task_node import TaskNode

class JSONStorage:
    """
    JSON-based storage service implementing:
    - Hash table (dict) for O(1) task lookup by ID
    - Tree structure for hierarchical relationships
    - Persistent storage with atomic writes
    """
    
    def __init__(self, storage_path: str = "data/tasks.json"):
        self.storage_path = storage_path
        self.tasks_by_id: Dict[str, Dict] = {}  # Hash table for O(1) lookup
        self.root_task_ids: List[str] = []      # List of root task IDs
        self._ensure_storage_directory()
        self.load_from_file()
    
    def _ensure_storage_directory(self):
        """Ensure the storage directory exists"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
    
    def save_to_file(self):
        """
        Atomic write to JSON file
        Uses temporary file + rename for atomicity
        """
        temp_path = self.storage_path + ".tmp"
        data = {
            "tasks": self.tasks_by_id,
            "root_task_ids": self.root_task_ids,
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "total_tasks": len(self.tasks_by_id),
                "version": "1.0"
            }
        }
        
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Atomic rename
            os.rename(temp_path, self.storage_path)
        except Exception as e:
            # Clean up temp file if it exists
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
    
    def load_from_file(self):
        """Load tasks from JSON file"""
        if not os.path.exists(self.storage_path):
            self.tasks_by_id = {}
            self.root_task_ids = []
            return
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.tasks_by_id = data.get("tasks", {})
            self.root_task_ids = data.get("root_task_ids", [])
        except (json.JSONDecodeError, FileNotFoundError):
            self.tasks_by_id = {}
            self.root_task_ids = []
    
    def add_task(self, task: TaskNode, parent_id: Optional[str] = None) -> bool:
        """
        Add task using hash table for O(1) insertion
        Maintains tree structure via parent-child relationships
        """
        task_data = {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "parent_id": parent_id,
            "completed": task.completed,
            "children": [],
            "created_at": datetime.now().isoformat()
        }
        
        # O(1) insertion into hash table
        self.tasks_by_id[task.id] = task_data
        
        if parent_id is None:
            # Root task - add to root list
            self.root_task_ids.append(task.id)
        else:
            # Child task - add to parent's children list
            if parent_id in self.tasks_by_id:
                self.tasks_by_id[parent_id]["children"].append(task.id)
                task_data["parent_id"] = parent_id
            else:
                return False
        
        self.save_to_file()
        return True
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """O(1) task retrieval using hash table"""
        return self.tasks_by_id.get(task_id)
    
    def update_task(self, task_id: str, updates: Dict[str, Any]) -> bool:
        """O(1) task update"""
        if task_id not in self.tasks_by_id:
            return False
        
        self.tasks_by_id[task_id].update(updates)
        self.tasks_by_id[task_id]["updated_at"] = datetime.now().isoformat()
        self.save_to_file()
        return True
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete task and all its children (recursive)
        Uses DFS traversal for deletion
        """
        if task_id not in self.tasks_by_id:
            return False
        
        task = self.tasks_by_id[task_id]
        
        # Recursively delete all children (DFS)
        for child_id in task.get("children", []):
            self.delete_task(child_id)
        
        # Remove from parent's children list
        parent_id = task.get("parent_id")
        if parent_id and parent_id in self.tasks_by_id:
            parent_children = self.tasks_by_id[parent_id]["children"]
            if task_id in parent_children:
                parent_children.remove(task_id)
        
        # Remove from root list if it's a root task
        if task_id in self.root_task_ids:
            self.root_task_ids.remove(task_id)
        
        # Remove from hash table
        del self.tasks_by_id[task_id]
        
        self.save_to_file()
        return True
    
    def get_all_tasks(self) -> List[Dict]:
        """
        Return all tasks in tree traversal order (DFS)
        Maintains hierarchical structure
        """
        def dfs_traverse(task_id: str, visited: set) -> List[Dict]:
            if task_id in visited or task_id not in self.tasks_by_id:
                return []
            
            visited.add(task_id)
            task = self.tasks_by_id[task_id].copy()
            result = [task]
            
            # Traverse children
            for child_id in task.get("children", []):
                result.extend(dfs_traverse(child_id, visited))
            
            return result
        
        all_tasks = []
        visited = set()
        
        # Start DFS from all root tasks
        for root_id in self.root_task_ids:
            all_tasks.extend(dfs_traverse(root_id, visited))
        
        return all_tasks
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get storage statistics and analytics"""
        total_tasks = len(self.tasks_by_id)
        completed_tasks = sum(1 for task in self.tasks_by_id.values() if task.get("completed", False))
        root_tasks = len(self.root_task_ids)
        
        # Calculate tree depth (BFS)
        max_depth = 0
        if self.root_task_ids:
            from collections import deque
            queue = deque([(root_id, 1) for root_id in self.root_task_ids])
            
            while queue:
                task_id, depth = queue.popleft()
                max_depth = max(max_depth, depth)
                
                if task_id in self.tasks_by_id:
                    for child_id in self.tasks_by_id[task_id].get("children", []):
                        queue.append((child_id, depth + 1))
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": total_tasks - completed_tasks,
            "root_tasks": root_tasks,
            "max_tree_depth": max_depth,
            "storage_size_bytes": os.path.getsize(self.storage_path) if os.path.exists(self.storage_path) else 0
        }
