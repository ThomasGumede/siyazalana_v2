import logging, json, base64
from celery import shared_task
from accounts.models import  Wallet
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from accounts.utilities.custom_emailing import send_html_email_with_attachments
from payments.models import SiyazalanaBank, PaymentInformation
from events.models import TicketOrderModel, reservation_time
from campaigns.models import ContributionModel, in_fourteen_days
from campaigns.utils import PaymentStatus
from django.template.loader import render_to_string
from django.template.loader import get_template
from weasyprint import HTML
from django.core.mail import EmailMessage
from django.conf import settings

logger = logging.getLogger("tasks")
event_logger = logging.getLogger("events")
campaign_logger = logging.getLogger("campaigns")
email_logger = logging.getLogger("emails")

def send_email_with_attachments(to_email:str, subject: str, html_content, from_email:str, pdf_attachments, pdf_name):
    try:
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email= from_email or settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.content_subtype = 'html'

        # Attach the file
        email.attach(pdf_name, pdf_attachments)
        email.attachments()

        # Send the email
        email.send()
        logger.info(f"Email sent to {to_email} with attachment.")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}. Error: {e}")
        return False

def send_tickets_email(status, order: TicketOrderModel, protocol, domain):
    try:
        invoice = get_template("emails/tickets/invoice.html")
        render_invoice = invoice.render({
                "buyer_full_name": order.buyer.get_full_name(),
                "order": order,
                "protocol": protocol,
                "domain": domain,
                "due_date": reservation_time(),
                
            })
        pdf_file = HTML(string=render_invoice).write_pdf()
        files = [
            (base64.b64encode(pdf_file).decode(), f'{order.order_number}_invoice.pdf')
        ]
        
        context = {
                    "protocol": protocol,
                    "domain": domain,
                    "user": order.buyer.get_full_name(),
                    "order": order,
                    # "facebook": COMPANY.facebook,
                    # "twitter": COMPANY.twitter,
                    # "linkedIn": COMPANY.linkedIn,
                    # "instagram": COMPANY.phone,
                    # "youtube": COMPANY.support_email, 
                    # "tiktok": COMPANY.address_one,
                    
                }
        if status == "payment.succeeded" or status == PaymentStatus.PAID:

            mail_subject = f"Your tickets for {order.event.title} on {order.event.date_time_formatter()}"
            message = render_to_string("emails/tickets/ticket-order-email.html", context,
            )
                    
            with open(order.tickets_pdf_file.path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()

            encoded_content = base64.b64encode(pdf_content).decode()
            
            files.append((encoded_content, f'{order.order_number}_tickets.pdf'))

        else:
            mail_subject = f"Your tickets order for {order.event.title} on {order.event.date_time_formatter()} was cancelled"
            message = render_to_string("emails/tickets/order-cancelled.html", context,
            )
           
        sent = send_html_email_with_attachments(order.email, mail_subject, message, "BBGI Events <events@bbgi.co.za>", files)
            
        if not sent:
            email_logger.error(f"Trouble sending tickets email to {order.email} order number {order.order_number}")

            return False
            
        return True
    
    except Exception as ex:
        logger.error(ex)
        return False

def send_contribution_confirm_email(order: ContributionModel, protocol, domain, status):
    try:
        template = get_template("emails/contributions/invoice-contribution.html")
        rendered_template = template.render({
                "buyer_full_name": order.contributor.get_full_name(),
                "order": order,
                "protocol": protocol,
                "domain": domain,
                "due_time": in_fourteen_days()
            })

        pdf_file = HTML(string=rendered_template).write_pdf()
        files = [
            (base64.b64encode(pdf_file).decode(), f'{order.order_number}_invoice.pdf')
        ]
        context = {
                        "protocol": protocol,
                        "domain": domain,
                        "user": order.contributor.get_full_name(),
                        "order": order,
                        # "facebook": COMPANY.facebook,
                        # "twitter": COMPANY.twitter,
                        # "linkedIn": COMPANY.linkedIn,
                        # "instagram": COMPANY.phone,
                        # "youtube": COMPANY.support_email, 
                        # "tiktok": COMPANY.address_one,
                    }

        if status == "payment.succeeded" or status == PaymentStatus.PAID:
            mail_subject = F"Your contribution confirmation {order.campaign.title} campaign was successful"
            message = render_to_string("emails/contributions/contribution-email.html",
                    context,
                )
        else:
            mail_subject = F"Your contribution payment {order.campaign.title} campaign was unsuccessful"
            message = render_to_string("emails/contributions/contribution-cancelled.html",
                    context,
                )


        sent = send_html_email_with_attachments(order.contributor.email, mail_subject, message, "BBGI Campaigns <campaigns@bbgi.co.za>", files)
          
        if not sent:
            email_logger.error(f"confirmation email not sent for {order.order_number} to {order.contributor.email}")
            return False
                
        return True

    except Exception as ex:
        logger.error(ex)   

def update_wallet(user, amount, tip, order_number, order_uuid):
    try:
        wallet, created = Wallet.objects.get_or_create(owner = user)
        if wallet:
            wallet.balance += amount
            wallet.save(update_fields=['balance'])
        if created:
            wallet.balance += amount
            wallet.save(update_fields=['balance'])
        
        SiyazalanaBank.objects.get_or_create(balance=tip, order_id=order_number, order_uuid=order_uuid)
        return True

    except Wallet.DoesNotExist:
        return False
    
def update_payment_details(order, data, payment_status: PaymentStatus):
    payload = data["payload"]
    payment_method_details = payload["paymentMethodDetails"]
    card_details = payment_method_details.get("card", None)
    order.paid = payment_status
    if card_details:
        order.payment_method_type = card_details.get("type", "-")
        order.payment_method_card_holder = card_details.get("cardHolder", "-")
        order.payment_method_masked_card = card_details.get("maskedCard", "-")
        order.payment_method_scheme = card_details.get("scheme", "-")

    order.payment_date = str(payload.get("createdDate", "-"))
    order.save(update_fields=["paid", "payment_method_card_holder", "payment_method_type","payment_method_masked_card", "payment_method_scheme"])

@shared_task
def update_payment_2_status(data, protocol, domain):
    payload = data["payload"]
    metadata = payload["metadata"]
    try:
        ticket_order = TicketOrderModel.objects.select_related("event", "buyer").get(checkout_id=metadata["checkoutId"])
        
        if data["type"] == "payment.succeeded":
            payment_status = PaymentStatus.PAID
            admin_cost = ticket_order.calculate_total_admin_cost()
            organiser_profit = ticket_order.calculate_actual_profit()
            wallet_updated = update_wallet(ticket_order.event.organiser, organiser_profit, admin_cost, ticket_order.order_number, ticket_order.id)
            if not wallet_updated:
                logger.error("Failed to update wallet")
        else:
            payment_status = PaymentStatus.NOT_PAID
        
        update_payment_details(ticket_order, data, payment_status)
        sent = send_tickets_email(data["type"], ticket_order, protocol, domain)

        if sent:
            return f"Tickets email - email was sent to {ticket_order.buyer.get_full_name()}"
        else:
            return f"Tickets email - email was not sent to {ticket_order.buyer.get_full_name()}"

    except TicketOrderModel.DoesNotExist:
        try:
            contribution = ContributionModel.objects.select_related("campaign", "contributor").get(checkout_id=metadata["checkoutId"], paid=PaymentStatus.PENDING)
            if data["type"] == "payment.succeeded":
                payment_status = PaymentStatus.PAID
                contribution.campaign.current_amount += contribution.amount
                contribution.campaign.save(update_fields=['current_amount'])
                tip = contribution.total_amount - contribution.amount
                wallet_updated = update_wallet(contribution.campaign.organiser, contribution.amount, tip, contribution.order_number, contribution.id)
                if not wallet_updated:
                    logger.error("Wallet not updated")
            else:
                payment_status = PaymentStatus.NOT_PAID

            update_payment_details(contribution, data, payment_status)
            sent = send_contribution_confirm_email(contribution, protocol, domain, data["type"])
            
            if sent:
                return f"Contribution confirmation email - email was sent to {contribution.contributor.get_full_name()}"
            else:
                return f"Contribution confirmation email - email was not sent to {contribution.contributor.get_full_name()}"
            
            
        except ContributionModel.DoesNotExist:
            pass
            # return f"Tickets email - email was not sent to {ticket_order.buyer.get_full_name()}"

@shared_task
def check_payment_update_2_contribution(checkout_id, protocol, domain):
    try:
        payment_information = PaymentInformation.objects.get(id=checkout_id)
        data = json.loads(payment_information.data)
        try:
            contribution = ContributionModel.objects.get(checkout_id=checkout_id)
            if data["type"] == "payment.succeeded":
                payment_status = PaymentStatus.PAID
                contribution.campaign.current_amount += contribution.amount
                contribution.campaign.save(update_fields=['current_amount'])
                tip = contribution.total_amount - contribution.amount
                wallet_updated = update_wallet(contribution.campaign.organiser, contribution.amount, tip, contribution.order_number, contribution.id)
                if not wallet_updated:
                    logger.error("Wallet not updated")
            else:
                payment_status = PaymentStatus.NOT_PAID

            update_payment_details(contribution, data, payment_status)
            sent = send_contribution_confirm_email(contribution, protocol, domain, data["type"])
            
            if sent:
                payment_information.order_number = contribution.order_number
                payment_information.order_updated = True
                payment_information.save(update_fields=["order_number", "order_updated"])
                return f"Contribution confirmation email - email was sent to {contribution.contributor.get_full_name()}"
            else:
                return f"Contribution confirmation email - email was not sent to {contribution.contributor.get_full_name()}"
            
        except ContributionModel.DoesNotExist:
            campaign_logger.error("Contribution not found")
            return f"Contribution {checkout_id} was not found"
        
    except PaymentInformation.DoesNotExist:
        pass


@shared_task
def check_payment_update_2_ticket_order(checkout_id, protocol, domain):
    try:
        payment_information = PaymentInformation.objects.get(id=checkout_id)
        data = json.loads(payment_information.data)
        try:
            ticket_order = TicketOrderModel.objects.get(checkout_id=checkout_id)
            if data["type"] == "payment.succeeded":
                payment_status = PaymentStatus.PAID
                admin_cost = ticket_order.calculate_total_admin_cost()
                organiser_profit = ticket_order.calculate_actual_profit()
                
                wallet_updated = update_wallet(ticket_order.event.organiser, organiser_profit, admin_cost, ticket_order.order_number, ticket_order.id)
                if not wallet_updated:
                    logger.error("Failed to update wallet")
            else:
                payment_status = PaymentStatus.NOT_PAID
        
            update_payment_details(ticket_order, data, payment_status)
            sent = send_tickets_email(data["type"], ticket_order, protocol, domain)

            if sent:
                payment_information.order_number = ticket_order.order_number
                payment_information.order_updated = True
                payment_information.save(update_fields=["order_number", "order_updated"])
                return f"Tickets email - email was sent to {ticket_order.buyer.get_full_name()}"
            else:
                return f"Tickets email - email was not sent to {ticket_order.buyer.get_full_name()}"
            
        except TicketOrderModel.DoesNotExist:
            event_logger.error(f"Ticket {checkout_id} order not found")
            return f"Ticket order {checkout_id} was not found"
        
    except PaymentInformation.DoesNotExist:
        pass

@shared_task
def resend_tickets_2_task(order_checkout, protocol, domain):
    try:
        order = TicketOrderModel.objects.get(checkout_id = order_checkout)
        sent = send_tickets_email(order.paid, order, protocol, domain)
        if not sent:
            return False
        
        return True

    except TicketOrderModel.DoesNotExist as ex:
        logger.error(f"Resend tickets - {ex}")
        return False