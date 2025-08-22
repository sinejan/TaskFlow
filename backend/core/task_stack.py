class TaskStack:
    def __init__(self):
        self.stack = []

    def push(self, task):
        self.stack.append(task)

    def pop(self):
        return self.stack.pop() if self.stack else None

    def peek(self):
        return self.stack[-1] if self.stack else None

    def is_empty(self):
        return len(self.stack) == 0
