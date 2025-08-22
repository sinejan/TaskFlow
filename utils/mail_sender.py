import smtplib
from email.mime.text import MIMEText

def send_email(to, subject, body, sender):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, "YOUR_APP_PASSWORD")  # Gmail'den alınan app-password
        server.send_message(msg)
        server.quit()
        print(f"[✔] Mail gönderildi: {to}")
    except Exception as e:
        print(f"[X] Mail gönderilemedi: {e}")
