class TaskTree:
    def __init__(self):
        self.root_tasks = []

    def add_task(self, task_node, parent_id=None):
        if parent_id is None:
            self.root_tasks.append(task_node)
        else:
            parent = self.find_by_id(parent_id)
            if parent:
                parent.add_child(task_node)
            else:
                raise ValueError("Parent bulunamadı.")

    def find_by_id(self, node_id):
        def dfs(nodes):
            for node in nodes:
                if node.id == node_id:
                    return node
                found = dfs(node.children)
                if found:
                    return found
            return None
        return dfs(self.root_tasks)

    def display(self):
        def _print(node, level=0):
            print("    " * level + f"- {node.name} (ID: {node.id})")
            for child in node.children:
                _print(child, level + 1)
        for root in self.root_tasks:
            _print(root)

    def remove_task(self, task_id):
        """Remove a task from the tree"""
        def remove_from_children(node):
            for i, child in enumerate(node.children):
                if child.id == task_id:
                    node.children.pop(i)
                    return True
                if remove_from_children(child):
                    return True
            return False

        # Check if it's a root task
        for i, root in enumerate(self.root_tasks):
            if root.id == task_id:
                self.root_tasks.pop(i)
                return True

        # Check if it's a child task
        for root in self.root_tasks:
            if remove_from_children(root):
                return True

        return False

    def get_all_tasks(self):
        def traverse(node):
            task_list = [{
                "id": node.id,
                "name": node.name,
                "description": node.description,
                "due_date": node.due_date,
                "parent_id": node.parent_id,
                "completed": node.completed,
                "children": [child.id for child in node.children]
            }]
            for child in node.children:
                task_list.extend(traverse(child))
            return task_list

        all_tasks = []
        for root in self.root_tasks:
            all_tasks.extend(traverse(root))
        return all_tasks
