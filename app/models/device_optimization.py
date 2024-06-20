from app import db
from PIL import Image
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import webbrowser

class DeviceOptimization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='device_optimizations')
    device_type = db.Column(db.String(50), nullable=False)
    optimization_settings = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<DeviceOptimization {self.device_type}>'

    def detect_device(self, user_agent):
        # Detect device type from user agent string
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
            template = template.replace('font-size:16px;', 'font-size:16px;')
        # More adjustments can be added here
        return template

    def optimize_images(self, images):
        # Optimize images for the device type
        optimized_images = []
        for image in images:
            if self.device_type == 'Mobile':
                optimized_images.append(self.reduce_image_size(image, 0.5))
            elif self.device_type == 'Tablet':
                optimized_images.append(self.reduce_image_size(image, 0.75))
            else:
                optimized_images.append(image)
        return optimized_images

    def reduce_image_size(self, image, factor):
        # Convert image to PIL format
        image = Image.open(BytesIO(image))
        # Resize image
        new_size = (int(image.width * factor), int(image.height * factor))
        image = image.resize(new_size, Image.ANTIALIAS)
        # Convert image back to binary format
        output = BytesIO()
        image.save(output, format=image.format)
        return output.getvalue()

    def set_font_size_and_line_height(self, template):
        # Set font size and line height for the email template
        if self.device_type == 'Mobile':
            template = template.replace('font-size:16px;', 'font-size:14px;')
            template = template.replace('line-height:1.5;', 'line-height:1.3;')
        elif self.device_type == 'Tablet':
            template = template.replace('font-size:16px;', 'font-size:15px;')
        elif self.device_type == 'Desktop':
            template = template.replace('font-sixe:16px;', 'font-size:16px;')
        return template

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

            # Open the email in a web browser (for demonstration purposes)
            self.open_in_browser(email, adjusted_template)

        except Exception as e:
            print(f"Failed to send test email: {e}")

    def open_in_browser(self, email, email_content):
        # Write email content to a temporary file
        tmp_file = 'test_email.html'
        with open(tmp_file, 'w', encoding='utf-8') as f:
            f.write(email_content)

        # Open the file in the default web browser
        webbrowser.open(f'file://{os.path.realpath(tmp_file)}')

    def optimize(self, user_agent, template, images, email):
        self.detect_device(user_agent)
        template = self.adjust_email_template(template)
        images = self.optimize_images(images)
        template = self.set_font_size_and_line_height(template)
        self.test_email(email)
        return template, images

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'device_type': self.device_type,
            'optimization_settings': self.optimization_settings,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
