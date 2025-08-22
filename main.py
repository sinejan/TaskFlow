from backend.core.task_node import TaskNode
from backend.core.task_tree import TaskTree
from backend.core.task_queue import TaskQueue
from backend.core.task_stack import TaskStack
from backend.core.thread_worker import ListenerThread, SenderThread
import time


# Yapılar
tree = TaskTree()
queue = TaskQueue()
stack = TaskStack()
processed_tasks = []

# Thread'leri başlat
listener = ListenerThread(queue, stack)
sender = SenderThread(stack, processed_tasks)

listener.start()
sender.start()

# Örnek task'ler
task1 = TaskNode("Ana Görev", "Ana görev açıklaması")
task2 = TaskNode("Alt Görev 1", "Queue kurulumu")
task3 = TaskNode("Alt Görev 2", "Stack kurulumu")

tree.add_task(task1)
tree.add_task(task2, parent_id=task1.id)
tree.add_task(task3, parent_id=task1.id)

# Taskleri queue'ya ekleyelim
queue.enqueue(task1)
queue.enqueue(task2)
queue.enqueue(task3)

# Task tree'yi gösterelim
tree.display()

# Main thread'i sonsuzda tut
while True:
    time.sleep(5)
