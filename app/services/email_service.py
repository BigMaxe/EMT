from flask_mail import Mail, Message
from app import app, config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

mail = Mail(app)

class EmailService:
    @staticmethod
    def send_email(subject, recipient, content):
        msg = Message(subject,
                      sender=config.MAIL_DEFAULT_SENDER,
                      recipients=[recipient])
        msg.body = content
        mail.send(msg)

    def send_bulk_email(self, subject, recipients, body):
        smtp_server = os.getenv('MAIL_SERVER')
        smtp_port = int(os.getenv('MAIL_PORT', 587))
        smtp_username = os.getenv('MAIL_USERNAME')
        smtp_password = os.getenv('MAIL_PASSWORD')

        for recipient in recipients:
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, recipient, msg.as_string())
