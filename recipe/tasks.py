import logging
from config.celery import celery_app
import celery
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config
import logging_config

logger = logging.getLogger(__name__)


@celery_app.task(base=celery.Task, queue='high')
def send_email(recipient_email, subject, body):
    smtp_server = config('SMTP_SERVER')
    port = config('SMTP_PORT')
    sender_email = config('EMAIL_USER')
    sender_password = config('EMAIL_PASSWORD')

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, recipient_email, text)
        logging.info("Email sent successfully!")
    except Exception as e:
        logger.error(f"Failed to send email: {e}", exc_info=True)
    finally:
        server.quit()
