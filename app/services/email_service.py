from flask_mail import Mail, Message
from app import app, config

mail = Mail(app)

class EmailService:
    @staticmethod
    def send_email(subject, recipient, content):
        msg = Message(subject,
                      sender=config.MAIL_DEFAULT_SENDER,
                      recipients=[recipient])
        msg.body = content
        mail.send(msg)
