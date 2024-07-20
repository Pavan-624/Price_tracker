import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables
env_data = os.getenv('ENV_DATA')

if env_data:
    env_vars = json.loads(env_data)
    print("Loaded environment variables")
else:
    raise ValueError("ENV_DATA is not set or empty")

from_email = env_vars.get('FROM_EMAIL', '')
from_password = env_vars.get('EMAIL_PASSWORD', '')
to_email = env_vars.get('TO_EMAIL', '')

smtp_server = 'smtp.gmail.com'
smtp_port = 587

def send_test_email():
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Test Email'
    body = 'This is a test email to check email functionality.'
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.send_message(msg)
            print(f"Test email sent to {to_email}")
    except Exception as e:
        print(f"An error occurred while sending email: {e}")

if __name__ == "__main__":
    send_test_email()
