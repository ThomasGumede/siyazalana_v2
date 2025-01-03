from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from siyazalana_home.utilities.decorators import user_not_superuser_or_staff
from campaigns.utils import PaymentStatus
from django.contrib.auth import get_user_model
from siyazalana_home.forms import EventUpdateStatusForm
from events.models import EventModel, TicketOrderModel
from django.contrib import messages
from django.db.models import Q

USER = get_user_model()

@login_required
@user_not_superuser_or_staff
def all_events(request, username=None):
    query = request.GET.get("query", None)
    queryset = EventModel.objects.all()
    if username:
        user = get_object_or_404(USER, username=username)
        if query:
            events = queryset.filter(Q(organiser = user) & Q(title__icontains=query)| Q(organiser__first_name__icontains=query))
        else:
            events = queryset.filter(organiser = user)
    else:
        if query:
            events = queryset.filter(Q(title__icontains=query)| Q(organiser__first_name__icontains=query))
        else:
            events = queryset

    return render(request, "dashboard/events/all-events.html", {"events": events, "query": query})


@login_required
@user_not_superuser_or_staff
def event_details(request, event_slug):
    queryset = EventModel.objects.all().select_related("organiser").prefetch_related("tickettypes", "ticket_orders")
    event = get_object_or_404(queryset, slug = event_slug)
    form = EventUpdateStatusForm(instance=event)
    total_sales = sum([order.total_price for order in event.ticket_orders.filter(paid = PaymentStatus.PAID)])
    total_seat_sold = sum([order.quantity for order in event.ticket_orders.filter(paid = PaymentStatus.PAID)])
    unsold_seats = sum([ticket_type.available_seats for ticket_type in event.tickettypes.all()])

    if request.method == "POST":
        form = EventUpdateStatusForm(instance=event, data=request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, "Event status was changed successfully")
            return redirect("siyazalana_home:event-details", event_slug=event.slug)
    

    return render(request, "dashboard/events/event-details.html", {"event": event, "total_seats": total_seat_sold, "sales": total_sales, "unsold_seats": unsold_seats, "form": form})

@login_required
@user_not_superuser_or_staff
def all_ticket_orders(request, event_id = None):
    ticketorders = TicketOrderModel.objects.all()
    event_model = None
    if event_id:
        event_model = get_object_or_404(EventModel, id=event_id)
        ticketorders = TicketOrderModel.objects.filter(event = event_model)
    

    return render(request, "dashboard/orders/orders.html", {"orders": ticketorders, "event": event_model})

@login_required
@user_not_superuser_or_staff
def ticket_order_details(request, order_id):
    order_queryset = TicketOrderModel.objects.select_related("event").prefetch_related("tickets")
    order = get_object_or_404(order_queryset, id=order_id)
    return render(request, "dashboard/orders/details.html", {"order": order})

@login_required
def delete_ticket_order(request, order_id):
    order = get_object_or_404(TicketOrderModel, id=order_id)
    if order.paid == PaymentStatus.PAID:
        messages.error(request, "You cannot delete order that is already paid")
        return redirect("siyazalana_home:all-ticket-orders")
    
    if request.method == 'POST':
        order.delete()
        messages.success(request, "Ticket order deleted successfully")
        return redirect("siyazalana_home:all-ticket-orders")
    return render(request, "events/event/delete.html", {"message": f"Are you sure you want to delete this order? {order.order_number}", "title": "Cancel ticket order"})

