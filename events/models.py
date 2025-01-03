import uuid
from decimal import Decimal
from accounts.custom_models.choices import StatusChoices
from accounts.models import AbstractCreate
from accounts.utilities.validators import verify_rsa_phone
from accounts.custom_models.abstracts import AbstractPayment
from campaigns.utils import generate_order_number, PaymentStatus
from siyazalana_home.models import BlogCategory
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField
from datetime import timedelta
from django.utils.safestring import mark_safe

PHONE_REGEX = verify_rsa_phone()

def handle_event_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"event/{filename}"

def reservation_time():
    return timezone.now() + timedelta(minutes=25)


class EventModel(AbstractCreate):
    category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT, related_name="events", null=True, blank=True)
    image = models.ImageField(help_text=_("Upload campaign image."), upload_to=handle_event_file_upload, null=True, blank=True)
    title = models.CharField(help_text=_("Enter title for your event"), max_length=150)
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    phone = models.CharField(help_text=_("Enter cellphone number"), max_length=15, validators=[PHONE_REGEX])
    email = models.EmailField()
    organiser = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None, related_name="events")
    small_description = models.TextField(help_text=_("Small description about your event for search"), null=True, blank=True)
    content = HTMLField()
    venue_name = models.CharField(max_length=400, help_text=_("Enter event venue name"), null=True, blank=True)
    event_address = models.CharField(max_length=300, help_text=_("Enter event address seperated by comma"), null=True, blank=True)
    map_coordinates  = models.CharField(max_length=300, blank=True, null=True)
    total_seats_sold = models.PositiveIntegerField(default=0)
    event_link = models.URLField(blank=True, null=True)
    event_startdate = models.DateTimeField(validators = [MinValueValidator(timezone.now(), "Event start date and time cannot be in the past")])
    event_enddate = models.DateTimeField(validators = [MinValueValidator(timezone.now(), "Event end date and time cannot be in the past")])
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.NOT_APPROVED)


    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def date_time_formatter(self):
        start_local = timezone.localtime(self.event_startdate)
        end_local = timezone.localtime(self.event_enddate)
        if start_local.date() == end_local.date():
            return f"{start_local.strftime('%a %d %b %Y')}, {start_local.strftime('%H:%M')} - {end_local.strftime('%H:%M')}"
        else:
            return f"{start_local.strftime('%a %d %b %Y, %H:%M')} - {end_local.strftime('%a %d %b %Y, %H:%M')}"
        
    def sales_days_left(self):
        date = self.event_enddate - timezone.now()
        if date.days < 0:
            return "0 days"
        if date.days > 1:
            return f"{date.days} days"
        else:
            return f"{date.days} day"

    def get_total_seats(self):
        total_seats = sum([ticket.available_seats for ticket in self.tickettypes.all()])
        return total_seats

    def __str__(self) -> str:
        return f"{self.title}"
    
    def get_average_rating(self):
        reviews = self.reviews.all()
        average_rating = reviews.aggregate(Avg('rating_value'))['rating_value__avg'] or 0
        text = round(average_rating, 1)
        
        return text
    
    def get_avg_rating(self):
        return self.reviews.aggregate(avg_rating_value=Avg('rating_value'))['avg_rating_value']
    
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe(f"<img src={self.image.url} alt={self.title}-image height='60' width='90' />")
        return ""

    def content_safe(self):
        return mark_safe(self.content)
    
    def get_absolute_url(self):
        return reverse("events:event-details", kwargs={"event_slug": self.slug})

    def request_payout_details(self):
        if self.status == StatusChoices.COMPLETED:
            pass

class EventContent(AbstractCreate):
    image = models.ImageField(help_text=_("Upload emages images."), upload_to=handle_event_file_upload)
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE, related_name="images")
    some_field = models.CharField(max_length=20, blank=True, null=True)

class EventReview(AbstractCreate):
    rating_value = models.IntegerField(validators=[
            MinValueValidator(0),   
            MaxValueValidator(5)  
        ])
    commenter = models.ForeignKey(get_user_model(), related_name="event_reviews", on_delete=models.SET_NULL, null=True)
    commenter_email = models.EmailField()
    commenter_full_names = models.CharField(max_length=300)
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE, related_name="reviews")
    comment_title = models.CharField(max_length=300)
    comment = models.TextField()

    class Meta:
        verbose_name = 'Ecent Review'
        verbose_name_plural = 'Ecent Reviews'

    def __str__(self) -> str:
        return self.commenter_email

class EventOrganisor(AbstractCreate):
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE, related_name="organisors")
    full_name = models.CharField(max_length=350)
    organisor_phone_one = models.CharField(max_length=15, validators=[PHONE_REGEX], unique=True, null=True, blank=True)
    organisor_email = models.EmailField(max_length=254)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Event Organisor'
        verbose_name_plural = 'Event Organisors'
        unique_together = ['full_name', 'organisor_phone_one', 'organisor_email']

class EventTicketTypeModel(AbstractCreate):
    title = models.CharField(max_length=250, help_text=_("Enter ticket type"))
    available_seats = models.PositiveIntegerField(default=0)
    sale_start = models.DateTimeField(null=True, blank=True, validators = [MinValueValidator(timezone.now(), "Ticket sale start date and time cannot be in the past")])
    sale_end = models.DateTimeField(null=True, blank=True, validators = [MinValueValidator(timezone.now(), "Ticket sale end date and time cannot be in the past")])
    price = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    transaction_cost = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    event = models.ForeignKey(EventModel, related_name="tickettypes", on_delete=models.CASCADE)


    def __str__(self) -> str:
        return f"{self.title} - R{self.price}(+ R{self.transaction_cost})"
    
    def sales_days_left(self):
        date = self.sale_end - timezone.now()
        if date.days < 0:
            return "0 days"
        if date.days > 1:
            return f"{date.days} days"
        else:
            return f"{date.days} day"
    
    def calculate_transaction_cost(self):
        cost = Decimal(self.price) * Decimal(3/100)
        return Decimal(round(cost, 2))
    
    def save(self, *args, **kwargs):
        self.transaction_cost = self.calculate_transaction_cost()
        self.total_price = self.calculate_transaction_cost() + Decimal(self.price)
        super(EventTicketTypeModel, self).save(*args, **kwargs)

class TicketOrderModel(AbstractCreate, AbstractPayment):
    order_number = models.CharField(max_length=300, editable=False, unique=True)
    checkout_id = models.CharField(max_length=200, unique=True, null=True, blank=True, db_index=True)

    client_first_name = models.CharField(max_length=250, null=True, blank=True)
    client_last_name = models.CharField(max_length=250, null=True, blank=True)
    client_phone = models.CharField(max_length=15, validators=[PHONE_REGEX], null=True, blank=True)
    client_email = models.EmailField(null=True, blank=True)

    client_address_one = models.CharField(max_length=300, blank=True, null=True)
    client_address_two = models.CharField(max_length=300, blank=True, null=True)
    client_city = models.CharField(max_length=300, blank=True, null=True)
    client_province = models.CharField(max_length=300, blank=True, null=True)
    client_country = models.CharField(max_length=300, default="South Africa")
    client_zipcode = models.BigIntegerField(blank=True, null=True)

    email = models.EmailField()
    coupon_code = models.CharField(max_length=300, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    order_note = models.TextField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=1000, decimal_places=2)
    total_transaction_costs = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    tip = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    accepted_laws = models.BooleanField(null=False, default=True)
    buyer = models.ForeignKey(get_user_model(), related_name="ticketorders", null=True, blank=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(EventModel, related_name="ticket_orders", on_delete=models.CASCADE)
    reservation_time = models.TimeField(default=reservation_time)
    paid = models.CharField(max_length=300, choices=PaymentStatus.choices, default=PaymentStatus.NOT_PAID)
    receipt = models.FileField(null=True, upload_to="tickets/invoice/")
    tickets_pdf_file = models.FileField(null=True, upload_to="tickets/pdf/")


    class Meta:
        verbose_name = 'Ticker order'
        verbose_name_plural = 'Ticker orders'

    def calculate_transaction_costs(self):
        cost = sum([ticket.ticket_type.transaction_cost for ticket in self.tickets.all()])
        return cost

    def calculate_total_admin_cost(self):
        cost = self.calculate_transaction_costs()
        return cost
    
    def calculate_actual_profit(self):
        profit = self.total_price - self.calculate_total_admin_cost()
        return profit
    
    def __str__(self) -> str:
        return self.order_number

    def get_client_full_name(self):
        return f"{self.client_first_name} {self.client_last_name}"
    
    def get_client_address(self):
        return f"{self.client_address_one}, {self.client_city}, {self.client_province}, {self.client_zipcode}"
    
    def get_absolute_url(self):
        return reverse("events:order", kwargs={"order_id": self.id, "event_slug": self.event.slug})
    
    def save(self, *args, **kwargs):
        self.order_number = generate_order_number(TicketOrderModel)
        super(TicketOrderModel, self).save(*args, **kwargs)

class TicketModel(AbstractCreate):
    guest_full_name = models.CharField(max_length=300, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    guest_phone_number = models.CharField(max_length=15, null=True, blank=True, validators=[PHONE_REGEX])
    quantity = models.PositiveBigIntegerField()
    ticket_type = models.ForeignKey(EventTicketTypeModel, related_name="tickets", on_delete=models.CASCADE)
    barcode_value = models.CharField(max_length=13, null=True, blank=True, unique=True)
    barcode_image = models.ImageField(upload_to='tickets/barcodes/', null=True, blank=True)
    qrcode_url = models.URLField(null=True, blank=True)
    qrcode_image = models.ImageField(upload_to='tickets/qrcodes/', null=True, blank=True)
    ticket_order = models.ForeignKey(TicketOrderModel, related_name="tickets", on_delete=models.CASCADE)
    scanned = models.BooleanField(default=False)
    scanned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
    
    def __str__(self) -> str:
        return "Ticket"

    def barcode_image_tag(self):
        if self.barcode_image.url is not None:
            return mark_safe(f"<img src={self.barcode_image.url} alt={self.id}-image height='60' width='60' />")
        return ""
    
    def qrcode_image_tag(self):
        if self.qrcode_image.url is not None:
            return mark_safe(f"<img src={self.qrcode_image.url} alt={self.id}-qrcode_image-image height='60' width='60' />")
        return ""

@receiver(pre_delete, sender=EventModel)
def delete_event_image_hook(sender, instance, using, **kwargs):
    instance.image.delete()

@receiver(pre_delete, sender=TicketOrderModel)
def delete_ticket_order_pdf(sender, instance: TicketOrderModel, using, **kwargs):
    if instance.tickets_pdf_file:
        instance.tickets_pdf_file.delete()

@receiver(post_save, sender=TicketModel)
def create_ticket(sender, instance, created, **kwargs):
    if created:
        ticket_type: EventTicketTypeModel = instance.ticket_type
        if ticket_type.available_seats > 0:
            ticket_type.available_seats -= instance.quantity
            ticket_type.save(update_fields=['available_seats'])
    

@receiver(pre_delete, sender=TicketModel)
def delete_ticket(sender, instance: TicketModel, using, **kwargs):
    ticket_type: EventTicketTypeModel = instance.ticket_type
    ticket_type.available_seats += instance.quantity
    ticket_type.save(update_fields=['available_seats'])
    if instance.barcode_image and instance.qrcode_image:
        instance.barcode_image.delete()
        instance.qrcode_image.delete()
    
    
@receiver(post_save, sender=TicketOrderModel)
def update_total_seats_avalaible(sender, instance: TicketOrderModel, created, **kwargs):
    if created:
        event: EventModel = instance.event
        event.total_seats_sold += instance.quantity
        event.save(update_fields=["total_seats_sold"])

@receiver(pre_delete, sender=TicketOrderModel)
def update_total_seats_avalaible_delete(sender, instance: TicketOrderModel, using, **kwargs):
    if instance.event.total_seats_sold > 0:
        instance.event.total_seats_sold -= instance.quantity
        instance.event.save(update_fields=["total_seats_sold"])


