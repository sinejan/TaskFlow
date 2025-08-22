from queue import Queue

class TaskQueue:
    def __init__(self):
        self.queue = Queue()

    def enqueue(self, task):
        self.queue.put(task)

    def dequeue(self):
        return self.queue.get() if not self.queue.empty() else None

    def is_empty(self):
        return self.queue.empty()
