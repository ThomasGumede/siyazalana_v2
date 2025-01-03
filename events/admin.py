from django.contrib import admin
# from events.tasks import notify_2_organiser_event_of_status_change
# from django.contrib.sites.shortcuts import get_current_site
from events.models import EventModel, TicketModel, TicketOrderModel, EventTicketTypeModel

# Actions
@admin.action(description="Approve selected events")
def make_approve(modeladmin, request, querset):
    querset.update(status="APPROVED")
    # for campaign in querset:
    #     notify_2_organiser_event_of_status_change.delay(campaign.id)

@admin.action(description="Pending selected events")
def make_pending(modeladmin, request, querset):
    querset.update(status="PENDING")
    # for campaign in querset:
    #     notify_2_organiser_event_of_status_change.delay(campaign.id)

class EventTicketTypeInline(admin.TabularInline):
    model = EventTicketTypeModel
    readonly_fields = ("event",)
    exclude = ("sale_start", "sale_end")
    extra = 0

class TicketOrderInline(admin.TabularInline):
    model = TicketOrderModel

class TicketInline(admin.TabularInline):
    model = TicketModel
    exclude = ("barcode_image", "barcode_value", "qrcode_image", "qrcode_url")
    extra = 0
    readonly_fields = ("id", "ticket_type","guest_full_name", "guest_email", "guest_phone_number", "quantity", "barcode_image_tag", "qrcode_image_tag")

@admin.register(TicketOrderModel)
class TicketOrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "checkout_id", "quantity", "subtotal", "buyer", "paid", "payment_date", "created")
    list_filter = ("order_number", "quantity", "paid", "created")
    date_hierarchy = "created"
    empty_value_display = "Empty"
    list_editable = ("paid", )
    search_fields = ("order_number", "checkout_id", "payment_date")
    inlines = [TicketInline]

@admin.register(EventModel)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "total_seats_sold", "category", "date_time_formatter", "status")
    exclude = ("title", "event_startdate", "event_enddate")
    list_editable = ("status",)
    list_per_page = 10
    search_fields = ("title",)
    list_filter = ("category", "created")
    actions = [make_approve, make_pending]
    inlines = [EventTicketTypeInline]
