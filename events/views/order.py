import logging, decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Prefetch, Q
from events.models import EventModel, TicketModel, TicketOrderModel, EventTicketTypeModel
from events.forms import TicketOrderForm, TicketForm, TicketOrderUpdateForm
from coupons.models import Coupon
from events.utils import generate_qr_and_bacode, generate_tickets_in_pdf
from accounts.custom_models.choices import StatusChoices
from campaigns.utils import PaymentStatus

logger = logging.getLogger("utils")

def generate_coupon_number() -> str:
    order_id_start = f'BBGICP{timezone.now().year}{timezone.now().month}'
    queryset = Coupon.objects.filter(code__iexact=order_id_start).count()
      
    count = 1
    code = order_id_start
    while(queryset):
        code = f'BBGICP{timezone.now().year}{timezone.now().month}{count}'
        count += 1
        queryset = Coupon.objects.all().filter(code__iexact=code).count()

    return code

def update_order_transaction_cost_subtotal(order_id) -> None:
    """
    Update the subtotal and transaction costs for a given order.
    """
    try:
        order = get_object_or_404(TicketOrderModel.objects.prefetch_related("tickets"), id=order_id)
        order.accepted_laws = True
        order.subtotal = sum(ticket.ticket_type.price for ticket in order.tickets.all())
        order.total_transaction_costs = sum(ticket.ticket_type.transaction_cost for ticket in order.tickets.all())
        order.save(update_fields=["total_transaction_costs", "subtotal", "accepted_laws"])
    except Exception as ex:
        logger.error(f"Failed to update order {order_id} transaction costs: {ex}")

def create_order_and_coupon(order_form: TicketOrderForm, request: HttpRequest, event: EventModel) -> TicketOrderModel:
    """
    Create a ticket order for a specific event.
    """
    order = order_form.save(commit=False)
    order.event = event
    order.buyer = request.user
    order.coupon_code = generate_coupon_number()
    order.save()
    Coupon.objects.get_or_create(code=order.coupon_code, discount=decimal.Decimal(50), valid_from=timezone.now(), valid_to=order.event.event_enddate, active=False)
    return order

def validate_tickets_quantity(forms, request: HttpRequest) -> bool:
    """
    Validate ticket quantities in the order forms.
    """
    custom_messages = []
    for form in forms:
        quantity = form.cleaned_data["quantity"]
        ticket_type: EventTicketTypeModel = form.cleaned_data["ticket_type"]

        plural = "are" if ticket_type.available_seats > 1 else "is only"
        if quantity > ticket_type.available_seats:
            custom_messages.append(
                f"Sorry, there {plural} {ticket_type.available_seats} seat(s) available in {ticket_type.title}"
            )

    if custom_messages:
        for message in custom_messages:
            messages.error(request, message)
        return False
    return True

def create_ticket(forms, order: TicketOrderModel, request: HttpRequest) -> bool:
    """
    Create tickets based on the provided forms and update the order.
    """
    try:
        for form in forms:
            quantity = form.cleaned_data["quantity"]
            ticket_type: EventTicketTypeModel = form.cleaned_data["ticket_type"]

            if ticket_type.sale_end <= timezone.now() and quantity > 0:
                messages.error(request, f"Sorry, ticket sale for <b>{ticket_type.title}</b> has ended")
                return False

            if quantity > 0:
                TicketModel.objects.bulk_create([
                    TicketModel(quantity=1, ticket_order=order, ticket_type=ticket_type)
                    for _ in range(int(quantity))
                ])

        update_order_transaction_cost_subtotal(order.id)
        generate_qr_and_bacode(order, request)
        messages.success(request, "Tickets were reserved successfully")
        return True
    except Exception as ex:
        messages.error(request, "Unable to generate tickets")
        logger.error(f"Failed to create tickets for order {order.id}: {ex}")
        return False

def ticket_order(request, order_id, event_slug):
    """
    View a specific ticket order.
    """
    event = get_object_or_404(EventModel, slug=event_slug)
    order = get_object_or_404(
        TicketOrderModel.objects.filter(event=event).prefetch_related("tickets"),
        id=order_id
    )
    return render(request, "events/orders/order.html", {"order": order})

@login_required
def ticket_orders(request, event_id=None):
    """
    List all ticket orders, optionally filtered by event.
    """
    event = None
    if event_id:
        event = get_object_or_404(EventModel, id=event_id, organiser=request.user)
        ticket_orders = TicketOrderModel.objects.filter(event=event)
    else:
        ticket_orders = TicketOrderModel.objects.filter(event__organiser=request.user).select_related('event').order_by("-event__created")

    return render(request, "events/orders/orders.html", {"orders": ticket_orders, "event": event})

@login_required
def create_ticket_order(request, event_slug):
    """
    Create a ticket order for an event.
    """
    queryset = EventModel.objects.filter(
        status=StatusChoices.APPROVED
    ).prefetch_related(
        Prefetch("tickettypes", queryset=EventTicketTypeModel.objects.filter(available_seats__gte=1, sale_start__lte=timezone.now(), sale_end__gte=timezone.now()))
    )
    event = get_object_or_404(queryset, slug=event_slug)
    time_remaining = (event.event_enddate - timezone.now()).days

    # if time_remaining <= 0 or event.get_total_seats() == 0:
    #     messages.error(request, "Sorry, this event is closed or has run out of tickets.")
    #     if time_remaining <= 0:
    #         event.status = StatusChoices.COMPLETED
    #         event.save(update_fields=["status"])
    #     return redirect("events:event-details", event_slug=event.slug)

    formset = formset_factory(TicketForm, extra=event.tickettypes.count(), max_num=event.tickettypes.count())

    if request.method == "POST":
        order_form = TicketOrderForm(request.POST)
        forms = formset(request.POST)

        if order_form.is_valid() and forms.is_valid():
            if validate_tickets_quantity(forms, request):
                order = create_order_and_coupon(order_form, request, event)
                if create_ticket(forms, order, request):
                    
                    return redirect("events:add-guests", ticket_order_id=order.id)
        messages.error(request, "Something went wrong. Please fix the errors below.")
    
    return render(request, "events/orders/create.html", {"forms": formset(), "order_form": TicketOrderForm(), "event": event})

@login_required
def add_guest_details(request, ticket_order_id):
    """
    Add guest details to a ticket order.
    """
    # check_ticket_order_payment.apply_async((ticket_order_id,), countdown=25 * 60)
    ticket_order = get_object_or_404(TicketOrderModel, buyer=request.user, id=ticket_order_id)
    tickets = TicketModel.objects.filter(ticket_order=ticket_order).select_related("ticket_type")
    formset = formset_factory(form=TicketForm, extra=tickets.count(), max_num=tickets.count())

    if request.method == 'POST':
        forms = formset(request.POST)
        if forms.is_valid():
            for form, ticket in zip(forms, tickets):
                ticket.guest_full_name = form.cleaned_data["guest_full_name"]
                ticket.guest_email = form.cleaned_data["guest_email"]
                ticket.save(update_fields=["guest_email", "guest_full_name"])

            if generate_tickets_in_pdf(ticket_order, request):
                messages.success(request, "Ticket holders added successfully")
            else:
                logger.error(f"Failed to generate tickets for order {ticket_order.order_number}")

            if ticket_order.total_price == 0.00:
                ticket_order.paid = PaymentStatus.PAID
                ticket_order.save()
                return redirect("events:order", event_slug=ticket_order.event.slug, order_id=ticket_order.id)

            return redirect("events:order-checkout", ticket_order_id=ticket_order.id)
        messages.error(request, "Please fix the errors below.")
    
    return render(request, "events/orders/add_guest_details.html", {"forms": formset(initial=tickets.values("ticket_type", "quantity")), "order": ticket_order})

@login_required
def order_checkout(request, ticket_order_id):
    ticket_order = get_object_or_404(TicketOrderModel, buyer=request.user, id=ticket_order_id)
    form = TicketOrderUpdateForm(instance=ticket_order)
    if request.method == "POST":
        form = TicketOrderUpdateForm(instance=ticket_order, data=request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated and ticket_order.buyer == None:
                order.buyer = request.user
            
            order.save()
            messages.success(request, "Billing details added successfully")
            return redirect("payments:ticket-payment", ticket_order_id=ticket_order.id)
        else:
            messages.error(request, "Something went wrong trying to checkout")
            return render(request, "events/orders/checkout.html", {"ticketorder": ticket_order, "form": form})
    return render(request, "events/orders/checkout.html", {"ticketorder": ticket_order, "form": form})

@login_required
def cancel_ticket_order(request, order_id):
    """
    Cancel a ticket order.
    """
    order = get_object_or_404(TicketOrderModel, buyer=request.user, id=order_id)
    return_url = "events:manage-ticket-orders"
    
    if order.paid in [PaymentStatus.PAID, PaymentStatus.PENDING]:
        messages.error(request, "You cannot delete an order that is already paid or pending.")
    else:
        order.delete()
        messages.success(request, "Ticket order cancelled successfully.")
    return redirect(return_url)
