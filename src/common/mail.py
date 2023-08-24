import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailManager():

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.smtp_server = "smtpout.secureserver.net"
            cls.smtp_port = "465"
            cls.smtp_username = "support@hireach.in"
            cls.smtp_password = "HiReach@2023l"
            cls.connection = None
            cls.sender = "Hireach Support"

        return cls._instance

    def ensure_connection(self):
        if not self.connection:
            print("ensure_connection", self.smtp_server, self.smtp_port)
            self.connection = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.connection.starttls()
            print("login", self.smtp_username, self.smtp_password)
            self.connection.login(self.smtp_username, self.smtp_password)

    def send_mail(self, subject, message, recipients):
        """
        Send an email.
        TODO: Need to add template support
        """
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        try:
            self.ensure_connection()
            print("Sending email to: ", recipients)
            self.connection.sendmail(
                self.smtp_username, recipients, msg.as_string())

        except Exception as e:
            print("Failed to send email:", e)

    def disconnect(self):
        if self.connection:
            self.connection.quit()
