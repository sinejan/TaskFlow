import threading
import time
from datetime import datetime
from utils.mail_sender import send_email

class DueDateChecker(threading.Thread):
    def __init__(self, tree, user_email, sender_email):
        super().__init__()
        self.tree = tree
        self.user_email = user_email
        self.sender_email = sender_email
        self.daemon = True

    def run(self):
        while True:
            self.check_due_dates()
            time.sleep(60)

    def check_due_dates(self):
        now = datetime.now()

        def check_node(node):
            if node.due_date and now >= node.due_date:
                send_email(
                    to=self.user_email,
                    subject="Task Due Reminder",
                    body=f"Görevin süresi doldu: {node.name}",
                    sender=self.sender_email
                )
            for child in node.children:
                check_node(child)

        for root in self.tree.root_tasks:
            check_node(root)
