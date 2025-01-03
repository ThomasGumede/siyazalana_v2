from django.urls import path
from events.views.event import create_event_address, delete_event_content, add_event_content, \
create_event, event_details, events, update_event, \
delete_event, add_event_organisor, update_event_organisor, delete_event_organisor, update_event_address

from events.views.order import create_ticket_order, add_guest_details, ticket_order, ticket_orders, cancel_ticket_order, order_checkout

from events.views.ticket_type import confirm_attandance, create_new_ticket_types, create_ticket_types, \
update_ticket_type, get_event_ticket_types, delete_ticket_type

from events.views.manage import manage_event, manage_events, manage_ticket_order, manage_ticket_orders, \
    generate_guest_list, generate_ticket

app_name = "events"
urlpatterns = [
    path("events/", events, name="events"),
    path("events/<slug:category_slug>", events, name="events-by-category"),
    path("event/get-started", create_event, name="create-event"),
    path("event/<slug:event_slug>/get-started", create_event, name="create-event-with-slug"),
    path("event/<slug:event_slug>/add-event-address", create_event_address, name="create-event-address"),
    path("event/<slug:event_slug>/add-event-tickets", create_new_ticket_types, name="add-event-tickets"),

    path("event/details/<slug:event_slug>", event_details, name="event-details"),
    path("event/update/<slug:event_slug>", update_event, name="update-event"),
    path("event/update-event-address/<slug:event_slug>", update_event_address, name="update-event-address"),
    path("event/delete/<slug:event_slug>", delete_event, name="delete-event"),
    path("account/events/manage", manage_events, name="manage-events"),
    path("account/events/manage/<slug:event_slug>", manage_event, name="manage-event"),
    path("dashboard/event/add-event-organisor/<slug:event_slug>", add_event_organisor, name="add-event-organisor"),
    path("dashboard/event/update-event-organisor/<slug:event_slug>/<uuid:organisor_id>", update_event_organisor, name="update-event-organisor"),
    path("dashboard/event/delete-event-organisor/<slug:event_slug>/<uuid:organisor_id>", delete_event_organisor, name="delete-event-organisor"),
    path("dashboard/event/update/content/<slug:event_slug>", add_event_content, name="add-event-content"),
    path("dashboard/delete/content/<slug:event_slug>/<uuid:content_id>", delete_event_content, name="delete-event-content"),
    path("ticket-types/<event_id>", get_event_ticket_types, name="event-ticket-types"),
    path("ticket-types/verify/<order_number>/<ticket_id>", confirm_attandance, name="confirm-attandance"),
    path("ticket-types/create/<event_id>", create_ticket_types, name="create-ticket-types"),
    path("ticket-types/update/<slug:event_slug>/<uuid:ticket_type_id>", update_ticket_type, name="update-ticket-type"),
    path("ticket-types/delete/<slug:event_slug>/<uuid:ticket_type_id>", delete_ticket_type, name="delete-ticket-type"),

    path("orders/all", ticket_orders, name="all-ticket-orders"),
    path("orders/all/<event_id>", ticket_orders, name="ticket-orders"),
    path("order/all/<slug:event_slug>/<uuid:order_id>", ticket_order, name="order"),
    path("order/generate/guest/<uuid:event_id>", generate_guest_list, name="generate-guest-list"),
    path("order/create/<slug:event_slug>", create_ticket_order, name="create-ticket-order"),
    path("order/cancel/<uuid:order_id>", cancel_ticket_order, name="cancel-ticket-order"),
    path("order/guest/<uuid:ticket_order_id>", add_guest_details, name="add-guests"),
    path("order/checkout/<uuid:ticket_order_id>", order_checkout, name="order-checkout"),
    path("account/order/manage", manage_ticket_orders, name="manage-ticket-orders"),
    path("account/order/manage/<uuid:order_id>", manage_ticket_order, name="manage-ticket-order"),
    path("account/order/generate/ticket/<uuid:order_id>/<uuid:ticket_id>", generate_ticket, name="generate-ticket")

    
    
]
