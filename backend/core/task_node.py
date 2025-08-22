from datetime import datetime
import uuid

class TaskNode:
    def __init__(self, name, description, due_date=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.due_date = None
        if due_date:
            self.due_date = datetime.fromisoformat(due_date)
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "children": [child.to_dict() for child in self.children]
        }
