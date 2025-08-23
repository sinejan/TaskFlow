from datetime import datetime
import uuid

class TaskNode:
    def __init__(self, name, description, due_date=None, parent_id=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.due_date = None
        if due_date:
            self.due_date = datetime.fromisoformat(due_date)
        self.children = []
        self.parent_id = parent_id
        self.completed = False

    def add_child(self, child_node):
        child_node.parent_id = self.id
        self.children.append(child_node)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "parent_id": self.parent_id,
            "completed": self.completed,
            "children": [child.to_dict() for child in self.children]
        }
