import hashlib
import base64
import hmac, logging, decimal
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from accounts.utilities.custom_emailing import send_html_email_with_attachments
from events.models import TicketOrderModel, reservation_time
from campaigns.models import ContributionModel, in_fourteen_days
from accounts.models import Wallet
from campaigns.utils import PaymentStatus
from events.models import TicketOrderModel
from django.conf import settings
from io import BytesIO
from django.template.loader import render_to_string
from django.template.loader import get_template
from weasyprint import HTML
from payments.models import SiyazalanaBank

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
    order.save(update_fields=["paid", "payment_date", "payment_method_card_holder", "payment_method_type","payment_method_masked_card", "payment_method_scheme"])
