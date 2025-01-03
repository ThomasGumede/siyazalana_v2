from datetime import timedelta
import decimal
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.custom_models.abstracts import AbstractPayment
from accounts.models import AbstractCreate
from accounts.utilities.validators import validate_fcbk_link, validate_insta_link, verify_rsa_phone, validate_in_link, validate_twitter_link
from campaigns.utils import handle_campaign_file_upload, PaymentStatus, Tip
from django.db import models
from django.utils import timezone
from accounts.custom_models.choices import StatusChoices
from siyazalana_home.models import BlogCategory
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField

User = get_user_model()
PHONE_REGEX = verify_rsa_phone()

def in_fourteen_days():
    return timezone.now() + timedelta(days=14)

def five_days():
    return timezone.now() + timedelta(days=5)

class CampaignModel(AbstractCreate):
    image = models.ImageField(help_text=_("Upload campaign image."), upload_to=handle_campaign_file_upload, blank=True, null=True)
    title = models.CharField(help_text=_("Enter title for your campaign"), max_length=150)
    slug = models.SlugField(max_length=250, blank=True)
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="campaigns")
    category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT, related_name="campaigns")
    small_description = models.TextField(help_text=_("Small description about your campaign for search optimization."), null=True, blank=True)
    details = HTMLField(help_text=_("Enter additional details about your campaign"))
    target = models.DecimalField(help_text=_("Enter target amount"),max_digits=1000, decimal_places=2, default=0.00)
    current_amount = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    phone = models.CharField(help_text=_("Enter cellphone number"), max_length=15, validators=[PHONE_REGEX], null=True, blank=True)
    alternative_phone = models.CharField(help_text=_("Enter your business number"), max_length=15, validators=[PHONE_REGEX], null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    facebook = models.URLField(validators=[validate_fcbk_link], blank=True, null=True)
    twitter = models.URLField(validators=[validate_twitter_link], blank=True, null=True)
    instagram = models.URLField(validators=[validate_insta_link], blank=True, null=True)
    linkedIn = models.URLField(validators=[validate_in_link], blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    campaign_address = models.CharField(max_length=300, help_text=_("Enter campaign address seperated by comma"), null=True, blank=True)
    map_coordinates  = models.CharField(max_length=300, blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=in_fourteen_days, validators=[MinValueValidator(timezone.now(), "Date should not be less that today's date")])
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.NOT_APPROVED)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Campaigns")
        verbose_name_plural = _("Campaigns")
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("campaigns:campaign", kwargs={"campaign_slug": self.slug})

    def get_days(self):
        date = self.end_date - timezone.now()
        if date.days < 0:
            return "0 days"
        if date.days > 1:
            return f"{date.days} days"
        else:
            return f"{date.days} day"

    def get_percentage_of_donated_fund(self):
        val = self.current_amount / self.target
        perc = val * 100
        if perc > decimal.Decimal(100):
            return round(100, 2)
        return round(perc, 2)
    

    def __str__(self):
        return str(self.title)
    
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe(f"<img src={self.image.url} alt={self.title}-image height='60' width='90' />")
        return ""
    
    def thumpnail(self):
        if self.image.url is not None:
            return mark_safe(f"<img src={self.image.url} alt={self.organiser.first_name}-image height='60' width='60' style='border-radius: 50%; height: 40px; width: 40px;' />")
        return ""

    def content_safe(self):
        return mark_safe(self.details)

class CampaignContent(AbstractCreate):
    image = models.ImageField(help_text=_("Upload emages images."), upload_to="campaigns/images/content/")
    campaign = models.ForeignKey(CampaignModel, on_delete=models.CASCADE, related_name="images")
    
    def __str__(self):
        return self.campaign.title + "content"
    
class CampaignReview(AbstractCreate):
    rating_value = models.IntegerField(validators=[
            MinValueValidator(0),   
            MaxValueValidator(5)  
        ])
    commenter = models.ForeignKey(get_user_model(), related_name="campaign_reviews", on_delete=models.SET_NULL, null=True)
    commenter_email = models.EmailField()
    commenter_full_names = models.CharField(max_length=300)
    campaign = models.ForeignKey(CampaignModel, on_delete=models.CASCADE, related_name="reviews")
    comment_title = models.CharField(max_length=250)
    comment = models.TextField()

    class Meta:
        verbose_name = 'Campaign Review'
        verbose_name_plural = 'Campaign Reviews'

    def __str__(self) -> str:
        return self.commenter_email
    
class CampaignUpdateModel(AbstractCreate):
    campaign = models.ForeignKey(CampaignModel, on_delete=models.CASCADE, related_name="updates")
    title = models.CharField(max_length=250)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Campaign Update'
        verbose_name_plural = 'Campaign Updates'

    def __str__(self) -> str:
        return f'Update for {self.campaign.title} - {self.created}'
    
class ContributionModel(AbstractCreate, AbstractPayment):
    order_number = models.CharField(max_length=300, editable=False, unique=True)
    checkout_id = models.CharField(max_length=200, unique=True, null=True, blank=True, db_index=True)
    amount = models.DecimalField(max_digits=1000, decimal_places=2, help_text=_("Enter contribution amount"))
    tip = models.CharField(default=Tip.TEN, max_length=25, choices=Tip.choices)
    total_amount = models.DecimalField(max_digits=1000, decimal_places=2)
    accepted_laws = models.BooleanField(default=True)
    message = models.TextField(blank=True, null=True)
    paid = models.CharField(max_length=40, choices=PaymentStatus.choices, default=PaymentStatus.NOT_PAID)
    campaign = models.ForeignKey(CampaignModel, on_delete=models.CASCADE, related_name="contributions")
    anonymous = models.BooleanField(default=False)
    contributor = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True, related_name="contributions")
    receipt = models.FileField(null=True, upload_to="contributions/receipts/")

    class Meta:
        verbose_name = _("Contribution")
        verbose_name_plural = _("Contributions")
        ordering = ["-created"]

    def calculate_tip_amount(self):
        if self.tip == "10%":
            tip_amount = decimal.Decimal(self.amount) * decimal.Decimal((10 / 100))
        elif self.tip == "15%":
            tip_amount = decimal.Decimal(self.amount) * decimal.Decimal((15 / 100))
        elif self.tip == "20%":
            tip_amount = decimal.Decimal(self.amount) * decimal.Decimal((20 / 100))
        else:
            tip_amount = decimal.Decimal(self.amount) * decimal.Decimal((25 / 100))
        return round(tip_amount, 2)

    def calculate_total(self):
        
        return decimal.Decimal(self.amount) + self.calculate_tip_amount()
    
    

    def __str__(self):
        return str(self.amount)
    
    def contribution_percentage(self):
        perc = (self.amount / self.campaign.target) * 100
        return f"{round(perc, 2)}%"
    
    def get_absolute_url(self):
        return reverse("campaigns:contribution", kwargs={"campaign_id": self.campaign.id, "contribution_id": self.id})
    

    def save(self, *args, **kwargs):
        self.total_amount = round(self.calculate_total(), 2)
        super(ContributionModel, self).save(*args, **kwargs)

@receiver(pre_delete, sender=CampaignModel)
def delete_campaign_image_hook(sender, instance, using, **kwargs):
    instance.image.delete()

@receiver(pre_delete, sender=ContributionModel)
def delete_campaign_image_hook(sender, instance, using, **kwargs):
    instance.receipt.delete()
