import hashlib
import base64
import hmac, logging, decimal
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.conf import settings
from accounts.utilities.custom_emailing import send_html_email_with_attachments, send_html_email
from events.models import TicketOrderModel, reservation_time
from campaigns.models import ContributionModel, in_fourteen_days
from campaigns.utils import PaymentStatus
from events.models import TicketOrderModel
from io import BytesIO
from django.template.loader import render_to_string
from django.template.loader import get_template
from weasyprint import HTML
email_logger = logging.getLogger("emails")

def send_tickets_email(status, order: TicketOrderModel, request):
    try:
        # Render invoice to PDF
        invoice_template = get_template("emails/tickets/invoice_v2.html")
        invoice_context = {
            "buyer_full_name": order.buyer.get_full_name(),
            "order": order,
            "due_date": reservation_time(),
        }
        render_invoice = invoice_template.render(invoice_context, request=request)
        pdf_file = HTML(string=render_invoice).write_pdf()
        
        # Save PDF to order's receipt
        buffer = BytesIO(pdf_file)
        order.receipt.save(f'{order.order_number}_invoice.pdf', buffer)
        
        # Prepare files for email attachments
        files = [{"file_content": base64.b64encode(pdf_file).decode(), "filename": f'{order.order_number}_invoice.pdf'}]

        context = {
            "user": order.buyer.get_full_name(),
            "order": order,
        }

        if status == "payment.succeeded" or status == PaymentStatus.PAID:
            mail_subject = f"Your tickets for {order.event.title} on {order.event.date_time_formatter()}"
            message_template = "emails/tickets/ticket-order-email.html"
            
            with open(order.tickets_pdf_file.path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
                encoded_content = base64.b64encode(pdf_content).decode()
                files.append({"file_content": encoded_content, "filename": f'{order.order_number}_tickets.pdf'})
        else:
            mail_subject = f"Your tickets order for {order.event.title} on {order.event.date_time_formatter()} was cancelled"
            message_template = "emails/tickets/order-cancelled.html"

        # Render email content
        message = render_to_string(message_template, context, request=request)

        # Send email with attachments
        sent = send_html_email_with_attachments(order.email, mail_subject, message, "BBGI Events <events@bbgi.co.za>", files)
        
        if not sent:
            email_logger.error(f"Failed to send tickets email to {order.email} for order number {order.order_number}")
            return False

        return True

    except Exception as ex:
        email_logger.error(f"Error in sending ticket email: {ex}")
        return False

def send_ticket_order_received_to_admin(order: TicketOrderModel, request):
    try:
        

        context = {
            
            "order": order,
        }

        
        mail_subject = f"Ticket order for {order.event.title} on {order.event.date_time_formatter()} was received"
        message_template = "emails/order-received.html"

        # Render email content
        message = render_to_string(message_template, context, request=request)

        # Send email with attachments
        email = EmailMessage(
            subject=mail_subject,
            body=message,
            from_email="BBGI Notifications <noreply@bbgi.co.za>",
            to=['gumedethomas12@gmail.com', 'finance@bbgi.co.za', 'events@bbgi.co.za'],
        )
        email.content_subtype = 'html'
        sent = email.send()
        
        if not sent:
            email_logger.error(f"Failed to send tickets email to 'gumedethomas12@gmail.com', 'finance@bbgi.co.za', 'sazi.ndwandwa@gmail.com' for order number {order.order_number}")
            return False

        return True

    except Exception as ex:
        email_logger.error(f"Error in sending ticket email to admin: {ex}")
        return False
    
def send_contribution_confirm_email(order: ContributionModel, request, status):
    try:
        # Render invoice to PDF
        template = get_template("emails/contributions/invoice-contribution.html")
        rendered_template = template.render({
            "buyer_full_name": order.contributor.get_full_name(),
            "order": order,
            "due_time": in_fourteen_days()
        }, request=request)
        
        pdf_file = HTML(string=rendered_template).write_pdf()
        buffer = BytesIO(pdf_file)
        order.receipt.save(f'{order.order_number}_invoice.pdf', buffer)
        
        # Prepare files for email attachments
        files = [{"file_content": base64.b64encode(pdf_file).decode(), "filename": f'{order.order_number}_invoice.pdf'}]
        context = {
            "user": order.contributor.get_full_name(),
            "order": order
        }

        if status == "payment.succeeded" or status == PaymentStatus.PAID:
            mail_subject = f"Your contribution confirmation for {order.campaign.title} campaign was successful"
            message_template = "emails/contributions/contribution-email.html"
        else:
            mail_subject = f"Your contribution payment for {order.campaign.title} campaign was unsuccessful"
            message_template = "emails/contributions/contribution-cancelled.html"

        # Render email content
        message = render_to_string(message_template, context, request=request)

        # Send email with attachments
        sent = send_html_email_with_attachments(order.contributor.email, mail_subject, message, "BBGI Campaigns <orders@bbgi.co.za>", files)
        
        if not sent:
            email_logger.error(f"Failed to send confirmation email for order {order.order_number} to {order.contributor.email}")
            return False

        return True

    except Exception as ex:
        email_logger.error(f"Error in sending contribution confirmation email: {ex}")
        return False



