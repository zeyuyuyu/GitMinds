import time
import os
import logging
import smtplib
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Configure email settings
EMAIL_FROM = 'alerts@gitminds.com'
EMAIL_TO = 'admin@gitminds.com'
EMAIL_SUBJECT = 'GitMinds Alert'

def monitor_system():
    """
    Continuously monitor system resources and send alerts if thresholds are exceeded.
    """
    while True:
        # Check CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > 90:
            send_alert(f'CPU usage is at {cpu_usage}%')

        # Check memory usage
        memory = psutil.virtual_memory()
        memory_usage = (memory.used / memory.total) * 100
        if memory_usage > 80:
            send_alert(f'Memory usage is at {memory_usage:.2f}%')

        # Check disk usage
        disk_usage = shutil.disk_usage('/')
        disk_percent = (disk_usage.used / disk_usage.total) * 100
        if disk_percent > 85:
            send_alert(f'Disk usage is at {disk_percent:.2f}%')

        time.sleep(60)  # Check every minute

def send_alert(message):
    """
    Send an email alert with the provided message.
    """
    msg = MIMEText(message)
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    with smtplib.SMTP('localhost') as smtp:
        smtp.send_message(msg)

    logging.info(f'Alert sent: {message}')

if __name__ == '__main__':
    monitor_system()