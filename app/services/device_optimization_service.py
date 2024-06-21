import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from requests.auth import HTTPBasicAuth
from flask import current_app

class DeviceOptimizationService:
    def __init__(self, device_type):
        self.device_type = device_type

    def detect_device(self, user_agent):
        # Implement logic to detect device from user agent string
        if 'Mobile' in user_agent:
            self.device_type = 'Mobile'
        elif 'Tablet' in user_agent:
            self.device_type = 'Tablet'
        else:
            self.device_type = 'Desktop'

    def adjust_email_template(self, template):
        # Adjust email template based on device type
        if self.device_type == 'Mobile':
            template = template.replace('font-size:16px;', 'font-size:14px;')
            template = template.replace('line-height:1.5;', 'line-height:1.3;')
        elif self.device_type == 'Tablet':
            template = template.replace('font-size:16px;', 'font-size:15px;')
        elif self.device_type == 'Desktop':
            template = template.replace('font-size:16px;', 'font-size:18px;')
            template = template.replace('line-height:1.5;', 'line-height:1.6;')
        return template

    def optimize_images(self, image_paths):
        optimized_images = []
        for path in image_paths:
            img = Image.open(path)
            if self.device_type == 'Mobile':
                img = img.resize((img.width // 2, img.height // 2))
            elif self.device_type == 'Tablet':
                img = img.resize((img.width * 3 // 4, img.height * 3 // 4))
            # Save optimized image
            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            optimized_images.append(buffer)
        return optimized_images

    def test_email(self, email):
        """
        Test email by sending a test email and checking the display on different devices.
        """
        # Example template
        email_template = """
        <html>
          <head></head>
          <body>
            <div style="font-size: 16px; line-height: 1.5;">
              <p>Hello, this is a test email.</p>
            </div>
          </body>
        </html>
        """

        # Adjust email template based on device type
        adjusted_template = self.adjust_email_template(email_template)

        # Setup the email message
        msg = MIMEMultipart()
        msg['From'] = os.getenv('MAIL_DEFAULT_SENDER')
        msg['To'] = email
        msg['Subject'] = 'Test Email'

        # Attach HTML content
        msg.attach(MIMEText(adjusted_template, 'html'))

        # Send the email
        try:
            smtp_server = os.getenv('MAIL_SERVER')
            smtp_port = int(os.getenv('MAIL_PORT', 587))
            smtp_username = os.getenv('MAIL_USERNAME')
            smtp_password = os.getenv('MAIL_PASSWORD')

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, email, msg.as_string())
            print(f"Test email sent successfully to {email}")
        except Exception as e:
            print(f"Failed to send test email: {e}")

        # Use Litmus to test email rendering
        litmus_username = os.getenv('LITMUS_USERNAME')
        litmus_password = os.getenv('LITMUS_PASSWORD')
        litmus_url = "https://api.litmus.com/v1/tests"

        payload = {
            'test_set': {
                'html': adjusted_template,
                'applications': ['applemail10', 'gmailnew', 'outlook16']
            }
        }

        try:
            response = requests.post(
                litmus_url,
                json=payload,
                auth=HTTPBasicAuth(litmus_username, litmus_password)
            )
            response.raise_for_status()
            test_result = response.json()
            print("Litmus test initiated successfully. Test ID:", test_result['id'])
            # Optionally, you can fetch the test results using the test ID
        except requests.exceptions.RequestException as e:
            print(f"Failed to initiate Litmus test: {e}")
