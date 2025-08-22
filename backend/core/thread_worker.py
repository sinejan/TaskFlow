import threading
import time
from .task_stack import TaskStack
from .task_queue import TaskQueue


class ListenerThread(threading.Thread):
    def __init__(self, queue: TaskQueue, stack: TaskStack):
        super().__init__()
        self.queue = queue
        self.stack = stack
        self.daemon = True

    def run(self):
        print("[🎧] Listener başlatıldı.")
        while True:
            if not self.queue.is_empty():
                task = self.queue.dequeue()
                print(f"[QUEUE ➜ STACK] Listener: Task alındı → {task.name}")
                self.stack.push(task)
            time.sleep(1)  # CPU dinlensin diye ufak bekleme


class SenderThread(threading.Thread):
    def __init__(self, stack: TaskStack, processed_tasks: list):
        super().__init__()
        self.stack = stack
        self.processed_tasks = processed_tasks
        self.daemon = True

    def run(self):
        print("[📤] Sender başlatıldı.")
        while True:
            if not self.stack.is_empty():
                task = self.stack.pop()
                print(f"[STACK ✔] Sender: Task işlendi → {task.name}")
                self.processed_tasks.append(task)
            time.sleep(2)
