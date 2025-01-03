import logging
from campaigns.models import ContributionModel
from campaigns.utils import PaymentStatus

from payments.utilities.custom_email import send_contribution_confirm_email
from payments.utilities.wallet_update_func import update_payment_details, update_wallet

logger = logging.getLogger("payments")

 
def update_payment_status_contribution_order(data, request, contribution: ContributionModel):

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
    sent = send_contribution_confirm_email(contribution, request, data["type"])

    if sent:
        return True
    else:
        return False

