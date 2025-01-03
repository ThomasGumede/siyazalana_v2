from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import logging

logger = logging.getLogger("tasks")
email_logger = logging.getLogger("emails")

 


def send_email_to_admin(subject, message, from_email, name):
    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=["gumedethomas12@gmail.com", "info@bbgi.co.za", "sazi.ndwandwa@gmail.com"]
        )
        if not email.send():
            return f"Email not sent from {from_email}"
        else:
            return "Email sent"
    except Exception as ex:
        logger.error(ex)
