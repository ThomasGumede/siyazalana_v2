from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch, Q
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.custom_models.choices import PaymentStatus
from events.models import EventModel, EventTicketTypeModel, TicketModel, TicketOrderModel
from events.forms import EventTicketTypeForm, EventTicketTypeUpdateForm
from django.contrib import messages
from django.utils import timezone

from events.utils import send_email_to_admins

def confirm_attandance(request, order_number, ticket_id):
    order = get_object_or_404(TicketOrderModel, order_number=order_number)
    if order.paid == PaymentStatus.PAID:
        ticket = get_object_or_404(TicketModel, id=ticket_id, ticket_order=order)
        if ticket.scanned == False:
            ticket.scanned = True
            ticket.scanned_at = timezone.now()
            ticket.save(update_fields=["scanned", "scanned_at"])
            messages.success(request, "Ticket valid and verified")
            return render(request, "events/ticket/confirm-attandee.html", {"ticket": ticket})
        else:
            messages.warning(request, f"Ticket already verified at {ticket.scanned_at}")
            return render(request, "events/ticket/already-verified.html", {"ticket": ticket})
    else:
        messages.error(request, "Unknown ticket")
        return redirect("siyazalana_home:siyazalana-home")


def get_event_ticket_types(request, event_id):
    try:
        event = EventModel.objects.get(id=event_id)
        event_ticket_types = EventTicketTypeModel.objects.filter(event = event, available_seats__gte=1, sale_start__lte=timezone.now(), sale_end__gte=timezone.now())

        json_event_ticket_types = serializers.serialize("json", event_ticket_types)
        return JsonResponse({"success": True, "event_ticket_types": json_event_ticket_types}, status=200)
    except EventModel.DoesNotExist:
        return JsonResponse({"success": False, "event_ticket_types": "Event does not exists"}, status=200)

@login_required
def create_new_ticket_types(request, event_slug):
    event = get_object_or_404(EventModel, organiser = request.user, slug = event_slug)
    
    
    if event.tickettypes.count() == 5:
        messages.error(request, "Cannot add another ticket type, it either you already have 5 tickets or there are no tickets available to allocate")
        return redirect("events:add-event-tickets", event.slug)
    
    if request.method == 'POST':
        
        form = EventTicketTypeForm(request.POST)

        if form.is_valid():
            add_another = form.cleaned_data.get("add_another", None)
            title = form.cleaned_data.get("title", None)
            ticket_type = form.save(commit=False)
            ticket_type.event = event
            ticket_type.save()
            
            if add_another:
                messages.success(request, f"Your Ticket type({title}) was successfully created")
                return redirect("events:add-event-tickets", event_slug=event.slug)
            
            messages.success(request, "Event created successfully and awaiting approval from our administration. It takes 4 - 24 hours to approve events")
            send_email_to_admins(event, request)
            return redirect("events:manage-event", event_slug=event.slug)
        else:
            messages.error(request, "Something is missing, please fix errors below")
            return render(request, "events/ticket/create-new-tickets-type.html", {"form": form, "event": event})
    else:    
        
        form = EventTicketTypeForm()
        return render(request, "events/ticket/create-new-tickets-type.html", {"form": form, "event": event})

@login_required
def create_ticket_types(request, event_id):
    event = get_object_or_404(EventModel, organiser = request.user, id = event_id)
    
    if event.tickettypes.count() == 5:
        messages.error(request, "Cannot add another ticket type, it either you already have 5 tickets or there are no tickets available to allocate")
        return redirect("events:manage-events")
    
    if request.method == 'POST':
        
        form = EventTicketTypeForm(request.POST)

        if form.is_valid():
            add_another = form.cleaned_data.get("add_another", None)
            title = form.cleaned_data.get("title", None)
            ticket_type = form.save(commit=False)
            ticket_type.event = event
            ticket_type.save()
            messages.success(request, f"Your Ticket type({title}) we successfully created")
            if add_another:
                return redirect("events:create-ticket-types", event_id=event.id)
            
            return redirect("events:manage-event", event_slug=event.slug)
        else:
            messages.error(request, "Something is missing, please fix errors below")
            return render(request, "events/ticket/create_tickets_type.html", {"form": form, "event": event})
    else:    
        
        form = EventTicketTypeForm()
        return render(request, "events/ticket/create_tickets_type.html", {"form": form, "event": event})
    
@login_required
def update_ticket_type(request, event_slug, ticket_type_id):
    event = get_object_or_404(EventModel, organiser = request.user, slug = event_slug)
    ticket = get_object_or_404(EventTicketTypeModel, event=event, id=ticket_type_id)
    
    if request.method == 'POST':
        form = EventTicketTypeUpdateForm(instance=ticket, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Ticket type {ticket.title} was updated successfully")
            return redirect("events:manage-event", event_slug=event.slug)
        else:
            messages.error(request, f"Ticket type {ticket.title} was not updated successfully. Fix errors below")
            return render(request, "events/ticket/update.html", {"form": form, "event": event })

    form = EventTicketTypeUpdateForm(instance=ticket)
    return render(request, "events/ticket/update.html", {"form": form, "event": event })

@login_required
def delete_ticket_type(request, event_slug, ticket_type_id):
    event = get_object_or_404(EventModel, organiser = request.user, slug = event_slug)
    
    ticket = get_object_or_404(EventTicketTypeModel, event=event, id=ticket_type_id)
    tickets = TicketModel.objects.filter(ticket_type=ticket)
    if tickets.count() > 0:
        messages.error(request, f"You cannot delete this ticket type because {tickets.count()} people have already paid for it")
        return redirect("events:manage-event", event_slug=event.slug)
    
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, "Ticket order deleted successfully")
        return redirect("events:manage-event", event_slug=event.slug)
    return render(request, "events/event/delete.html", {"message": f"Are you sure you want to delete this ticket type? {ticket.title}", "title": "Delete ticket type"})

