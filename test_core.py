import time
from backend.core.task_node import TaskNode
from  backend.core.task_queue import TaskQueue
from  backend.core.task_stack import TaskStack
from  backend.core.thread_worker import ListenerThread, SenderThread
import time

def main():
    # Queue ve Stack oluştur
    queue = TaskQueue()
    stack = TaskStack()
    processed_tasks = []

    # Listener ve Sender thread'leri başlat
    listener = ListenerThread(queue, stack)
    sender = SenderThread(stack, processed_tasks)

    listener.start()
    sender.start()

    # Test için örnek tasklar oluştur ve queue'ya ekle
    print("[TEST] Görevler sıraya ekleniyor...")
    for i in range(3):
        task = TaskNode(name=f"Task-{i+1}", description=f"Test Görevi {i+1}")
        queue.enqueue(task)
        print(f"[TEST] Görev eklendi: {task}")

    # Thread'lerin çalışması için biraz zaman tanı
    time.sleep(3)

    # İşlenen görevleri yazdır
    print(f"[TEST] İşlenen görevler sayısı: {len(processed_tasks)}")
    for t in processed_tasks:
        print(f"[TEST] İşlenen: {t}")

    # Thread'leri kapatmak için (güvenli kapanma yoksa, script sonlandırılır)
    # Burada basitçe main bitince thread'ler de bitebilir.

if __name__ == "__main__":
    main()
