import threading
import time
from datetime import datetime
import smtplib
from email.message import EmailMessage

class AlarmThread(threading.Thread):
    def __init__(self, task_tree, check_interval=30, alarm_before=60):
        super().__init__()
        self.task_tree = task_tree
        self.check_interval = check_interval
        self.alarm_before = alarm_before
        self.running = True

        # Kendi gmail bilgilerinle değiştir
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.email_user = 'meseyeaydin@gmail.com'  # Buraya kendi mailin
        self.email_password = 'Adamlarsiniz34.'   # Gmail uygulama şifren
        self.email_to = 'sehra2002eser@gmail.com'  # Kullanıcı maili

    def send_email(self, subject, body):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.email_user
        msg['To'] = self.email_to
        msg.set_content(body)

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
            smtp.starttls()
            smtp.login(self.email_user, self.email_password)
            smtp.send_message(msg)
            print(f"[ALARM] Email gönderildi: {subject}")

    def run(self):
        while self.running:
            now = datetime.now()
            tasks = self.task_tree.get_all_tasks()
            for t in tasks:
                due_date_str = t.get('due_date')
                if due_date_str:
                    due_date = datetime.fromisoformat(due_date_str)
                    diff = (due_date - now).total_seconds()
                    if 0 < diff <= self.alarm_before:
                        subject = f"Görev Yaklaşıyor: {t['name']}"
                        body = f"'{t['name']}' görevine son {self.alarm_before} saniye kaldı: {due_date_str}"
                        self.send_email(subject, body)
            time.sleep(self.check_interval)

    def stop(self):
        self.running = False
