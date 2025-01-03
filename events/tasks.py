from celery import shared_task
import logging
from accounts.custom_models.choices import StatusChoices
from events.models import TicketOrderModel, EventModel
from campaigns.tasks import update_status_email
from django.utils import timezone
from campaigns.utils import PaymentStatus

    
logger = logging.getLogger("tasks")

@shared_task
def check_ticket_2_order_payment(order_id):
    try:
        order = TicketOrderModel.objects.get(id=order_id)
        if order.paid == PaymentStatus.NOT_PAID:
            order.delete()
        
            return f"{order_id} was deleted"
    
    except TicketOrderModel.DoesNotExist:
        pass


@shared_task
def check_2_events_status():
    now = timezone.now()
    events = EventModel.objects.filter(event_enddate__lte=now)

    for event in events:
        if event.status != StatusChoices.COMPLETED:
            event.status = StatusChoices.COMPLETED
            event.save(update_fields=["status"])
            if not update_status_email("Event", event):
                logger.error("Failed to send email of Event status change")

    f"{events.count()} events were marked at completed"

@shared_task
def notify_2_organiser_event_of_status_change(event_id, domain = 'bbgi.co.za', protocol = 'https'):
    try:
        
        event = EventModel.objects.select_related("organiser").get(id=event_id)
        if not update_status_email("Event", event, domain, protocol):
            logger.error(f"Failed to send event status update - id {event.id}")

        return "Done"
    
    except EventModel.DoesNotExist:
        pass
