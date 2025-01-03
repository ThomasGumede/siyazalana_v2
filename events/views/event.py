from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.custom_models.choices import StatusChoices
from siyazalana_home.models import BlogCategory
from events.models import EventContent, EventModel, EventOrganisor
from campaigns.utils import generate_slug, PaymentStatus
from events.forms import EventAddressForm, EventCreateForm, EventForm, EventOrganisorForm, EventReviewForm
from django.contrib import messages
from django.db.models import Q, When, Case


def events(request, category_slug=None):
    query = request.GET.get("query", None)
    place = request.GET.get("place", None)
    sort_by = request.GET.get("sort_by", None)
    queryset = EventModel.objects.filter(Q(status = StatusChoices.APPROVED) | Q(status = StatusChoices.COMPLETED))
    if category_slug:
        category = get_object_or_404(BlogCategory, slug=category_slug)
        if query:
            events = queryset.filter(Q(category = category) & Q(title__icontains=query)| Q(organiser__first_name__icontains=query) | Q(event_address__icontains=place or query))
        else:
            events = queryset.filter(category = category)
    else:
        if query:
            events = queryset.filter(Q(title__icontains=query)| Q(organiser__first_name__icontains=query))
        else:
            events = queryset
    if sort_by == 'newest':
        events = events.order_by('-created')
        
    context = {
        "events": events, 
        "query": query,
        "place": place,
        "sort_by": sort_by,
        "category": category_slug
    }

    return render(request, "events/event/list.html", {"events": events, "query": query})

def event_details(request, event_slug):
    queryset = EventModel.objects.all().select_related("organiser").prefetch_related("images")
    event = get_object_or_404(queryset, slug = event_slug)
    form = EventReviewForm()
    recent_events = EventModel.objects.all().order_by("-created")[:6]
    if event.status == StatusChoices.NOT_APPROVED or event.status == StatusChoices.BLOCKED:
        messages.info(request, "This event is either not approved or blocked. Please contact the event organisors before purchasing tickets")
    for event_file in event.images.all():
        print(f"{event_file.image.url}")
        print("6")
        
    if request.method == "POST":
        form = EventReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.event = event
            if request.user.is_authenticated:
                review.commenter = request.user
            review.save()
            messages.success(request, "Review added successfully")
            
        else:
            messages.error(request, "Error trying to add your review")
            
    return render(request, "events/event/details-v2.html", {"event": event, "form": form})

@login_required
def create_event(request, event_slug=None):
    if event_slug:
        event = get_object_or_404(EventModel, slug=event_slug, organiser=request.user)
        if request.method == "POST":
            form = EventCreateForm(instance=event, data=request.POST, files=request.FILES)
            if form.is_valid() and form.is_multipart():
                # event = form.save(commit=False)
                form.save()
                messages.success(request, "Event was added successfully")
                return redirect("events:create-event-address", event_slug=event.slug)
            else:
                
                messages.error(request, "Please fix below errors")
                return render(request, "events/event/create.html", {"form": form })
            
        form = EventCreateForm(instance=event)
        return render(request, "events/event/create.html", {"form": form })
    else:
        if request.method == "POST":
            form = EventCreateForm(request.POST, request.FILES)
            if form.is_valid() and form.is_multipart():
                event = form.save(commit=False)
                event.organiser = request.user
                event.slug = generate_slug(form.cleaned_data["title"], EventModel)
                event.save()
                messages.success(request, "Event was added successfully")
                return redirect("events:create-event-address", event_slug=event.slug)
            else:
                
                messages.error(request, "Please fix below errors")
                return render(request, "events/event/create.html", {"form": form })
        form = EventCreateForm()
        return render(request, "events/event/create.html", {"form": form })

@login_required
def create_event_address(request, event_slug):
    event = get_object_or_404(EventModel, slug=event_slug, organiser=request.user)
    form = EventAddressForm(instance=event)
    if request.method == "POST":
        form = EventAddressForm(instance=event, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event address added successfully!")
            return redirect("events:add-event-tickets", event.slug)
        else:
            messages.error(request, "Error occured trying to add event address")

    return render(request, "events/event/create-event-address.html", {"form": form, "event": event })

@login_required
def update_event(request, event_slug):
    event = get_object_or_404(EventModel, organiser = request.user, slug = event_slug)
    if request.method == "POST":
        form = EventCreateForm(instance=event, data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            
            event = form.save(commit=False)
            event.save()
            messages.success(request, "Event details was updated successfully")
            return redirect("events:manage-event", event.slug)
        else:
            messages.error(request, "Please fix below errors")
            return render(request, "events/event/update/update-event-details.html", {"form": form, "event": event })
        
    form = EventCreateForm(instance=event)
    return render(request, "events/event/update/update-event-details.html", {"form": form, "event": event })

@login_required
def update_event_address(request, event_slug):
    event = get_object_or_404(EventModel, slug=event_slug, organiser=request.user)
    form = EventAddressForm(instance=event)
    if request.method == "POST":
        form = EventAddressForm(instance=event, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event address updated successfully!")
            return redirect("events:update-event-tickets", event.slug)
        else:
            messages.error(request, "Error occured trying to add event address")

    return render(request, "events/event/update/update-event-address.html", {"form": form, "event": event })

@login_required
def add_event_content(request, event_slug):
    event = get_object_or_404(EventModel, organiser = request.user, slug = event_slug)
    if request.method == "POST":
        files = request.FILES.getlist("files")
        if len(files) > 0:
            for file in files:
                    event_content = EventContent(image=file, event=event)
                    event_content.save()
            messages.success(request, "Event images added successfully")
            return redirect("events:add-event-content", event.slug)
        else:
            messages.error(request, "Please select atleast one image before submiting form")
            return render(request, "events/event/manage/update-event-content.html", {"event": event})
        
    return render(request, "events/event/manage/update-event-content.html", {"event": event})

@login_required
def delete_event_content(request, event_slug, content_id):
    
    event = get_object_or_404(EventModel, organiser = request.user, slug = event_slug)
    content = get_object_or_404(EventContent, id=content_id, event=event)
    content.delete()
    messages.success(request, "Image removed successfully")
    return redirect("events:add-event-content", event.slug)

@login_required
def delete_event(request, event_slug):
    event = get_object_or_404(EventModel.objects.prefetch_related("ticket_orders"), organiser = request.user, slug = event_slug)

    if event.total_seats_sold / event.get_total_seats() == 0.25 or event.ticket_orders.filter(Q(paid = PaymentStatus.PENDING)| Q(paid = PaymentStatus.PAID)).count() > 0:
        messages.warning(request, "Because of our no refund policy, You cannot delete an event that has pending or paid tickets orders!")
        return redirect("events:manage-events")
    if request.method == "POST":
        event.delete()
        
        messages.success(request, "Event deleted successfully")
        return redirect("events:manage-events")
    return render(request, "events/event/delete.html", {"message": f"Are you sure you want to delete this event ({event.title})?", "title": "Delete event"})

@login_required
def add_event_organisor(request, event_slug):
    event = get_object_or_404(EventModel, slug=event_slug, organiser=request.user)
    if request.method == "POST":
        form = EventOrganisorForm(data=request.POST)
        if form.is_valid():
            add_another = form.cleaned_data.get("add_another", None)
            organisor = form.save(commit=False)
            organisor.event = event
            organisor.save()
            messages.success(request, "Event organisor added successfully")
            if add_another:
                return redirect("events:add-event-organisor", event_slug=event.slug)
            
            return redirect("events:manage-event", event_slug=event.slug)
        else:
            return render(request, "events/event/manage/add-event-organisor.html", {"form": form, "event": event})
        
    form = EventOrganisorForm()
    return render(request, "events/event/manage/add-event-organisor.html", {"form": form, "event": event})

@login_required
def update_event_organisor(request, event_slug, organisor_id):
    event = get_object_or_404(EventModel, slug=event_slug, organiser=request.user)
    organisor = get_object_or_404(EventOrganisor, id=organisor_id)
    if request.method == "POST":
        form = EventOrganisorForm(instance=organisor, data=request.POST)
        if form.is_valid():
            add_another = form.cleaned_data.get("add_another", None)
            form.save()
            messages.success(request, "Event organisor updated successfully")
            if add_another:
                return redirect("events:add-event-organisor", event_slug=event.slug)
            
            return redirect("events:manage-event", event_slug=event.slug)
        else:
            return render(request, "events/event/manage/update-event-organisor.html", {"form": form, "event": event})
        
    form = EventOrganisorForm(instance=organisor)
    return render(request, "events/event/manage/update-event-organisor.html", {"form": form, "event": event}) 


@login_required
def delete_event_organisor(request, event_slug, organisor_id):
    event = get_object_or_404(EventModel, slug=event_slug, organiser=request.user)
    organisor = get_object_or_404(EventOrganisor, id=organisor_id)
    
    organisor.delete()
    messages.success(request, "Event organisor deleted successfully")
    return redirect("events:manage-event", event_slug=event.slug)
