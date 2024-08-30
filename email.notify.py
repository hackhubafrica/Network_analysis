import smtplib
from email.mime.text import MIMEText

def send_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'your-email@example.com'
    msg['To'] = 'admin@example.com'

    with smtplib.SMTP('smtp.example.com') as server:
        server.login('your-email@example.com', 'your-password')
        server.send_message(msg)