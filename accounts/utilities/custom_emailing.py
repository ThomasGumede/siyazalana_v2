import logging, base64
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from accounts.utilities.tokens import account_activation_token, generate_activation_token
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.conf import settings
from smtplib import SMTPException

email_logger = logging.getLogger("emails")
accounts_logger = logging.getLogger("accounts")

def send_email_confirmation_email(user, new_email, request):
    try:
        mail_subject = "Siyazalana | New Email Confirmation"
        message = render_to_string("emails/account/email_activation.html",
                {
                    "user": user.get_full_name(),
                    "email": new_email,
                    "uid": generate_activation_token(user),
                    "token": account_activation_token.make_token(user),
                }, request
            )

        email = EmailMessage(
                subject=mail_subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
        email.content_subtype = 'html' 

            # Send the email
        email.send()
        email_logger.info(f"Email sent to {user.email} without attachment.")
            
        return True
    except Exception as err:
        email_logger.error(f"Failed to send send_email_confirmation_email to {user.email}. Error: {err}")
        return False
    

def send_verification_email(user, request):
    try:
        
        mail_subject = "Siyazalana | Activate Your Account"
        uid = generate_activation_token(user)
        token = account_activation_token.make_token(user)
        activation_link = request.build_absolute_uri(reverse("accounts:activate", kwargs={"uidb64": uid, "token": token}))

        message = render_to_string(
            "emails/account/account_activate_email.html",
            {
                "user": user.get_full_name(),
                "activation_link": activation_link,
            }
        )

        # Email configuration
        email = EmailMessage(
            subject=mail_subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.content_subtype = "html"

        # Send the email
        email.send()
        email_logger.info(f"Verification email sent to {user.email}.")
        return True
    except SMTPException as smtp_err:
        email_logger.error(
            f"SMTPException while sending email to {user.email}: {smtp_err}"
        )
    except Exception as err:
        email_logger.error(
            f"Failed to send verification email to {user.email}. Error: {err}"
        )
    return False


def send_password_reset_email(user, request):
    try:
        mail_subject = "Siyazalana | Password Reset request"
        message = render_to_string("emails/password/reset_password_email.html", {
            'user': user.get_full_name(),     
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }, request)
            
            
        # sent = custom_send_email(user.email, subject, message)
        # if not sent:
        #     return False
           
        email = EmailMessage(
                subject=mail_subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
        email.content_subtype = 'html' 

            # Send the email
        email.send()
        email_logger.info(f"Email sent to {user.email} without attachment.")
            
        return True
    except Exception as err:
        email_logger.error(f"Failed to send send_password_reset_email to {user.email}. Error: {err}")
        return False

def custom_send_email(to_email, subject, html_content):
    # message = Mail(
    #     from_email='Black Business Growth Initiative <noreply@bbgi.co.za>',
    #     to_emails=to_email,
    #     subject=subject,
    #     html_content=html_content,
    # )

    try:
        # sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        # response = sg.send(message)
        return True
    
    except Exception as e:
        # logger.error(f"Error sending email: {e}")
        return False

