import logging
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rx_newsletter.settings import EMAIL_HOST, EMAIL_PASSWORD, EMAIL_PORT, EMAIL_SMTP_SERVER

logger = logging.getLogger(__name__)


class EmailSender(object):
    instance = None

    def __init__(self, email, password) -> None:
        self.email = email 
        self.password = password

    def send_email(self, receiver_email, message):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(EMAIL_SMTP_SERVER, EMAIL_PORT, context=context) as server:
            server.login(self.email, self.password)
            server.sendmail(self.email, receiver_email, message)
            logger.info(f" Email send to {receiver_email}")

    def send_email_with_html(self, receiver_email, subject, message_text, html):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.email
        message["To"] = receiver_email

        part1 = MIMEText(message_text, "plain", "utf-8")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        self.send_email(receiver_email, message.as_bytes())

    @classmethod
    def base(cls):
        if cls.instance is None:
            cls.instance = cls(email=EMAIL_HOST, password=EMAIL_PASSWORD)

        return cls.instance
