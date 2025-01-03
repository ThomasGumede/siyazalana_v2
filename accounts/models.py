from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete, post_save
from accounts.utilities.abstracts import AbstractCreate, AbstractProfile
from accounts.utilities.choices import TITLE_CHOICES, WALLET_STATUS, IdentityNumberChoices, StatusChoices
from accounts.utilities.file_handlers import handle_profile_upload, handle_verification_docs_upload
from accounts.utilities.validators import verify_rsa_phone

PHONE_VALIDATOR = verify_rsa_phone()

class Wallet(AbstractCreate):
    name = models.CharField(max_length=250)
    balance = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    owner = models.OneToOneField("Account", on_delete=models.CASCADE, related_name="my_wallet")
    status = models.CharField(max_length=150, choices=WALLET_STATUS, default=WALLET_STATUS[0])
    cleared_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")
        ordering = ["-created"]

    def request_payout_details(self):
        pass

    def clear_account(self):
        self.balance = 0

    def __str__(self):
        return self.name

class Account(AbstractUser, AbstractProfile):
    profile_image = models.ImageField(help_text=_("Upload profile image"), upload_to=handle_profile_upload, null=True, blank=True)
    title = models.CharField(max_length=30, choices=TITLE_CHOICES)
    maiden_name = models.CharField(help_text=_("Enter your maiden name"), max_length=300, blank=True, null=True)
    occupation = models.CharField(default='N/A',help_text=_("Enter your current employment"), max_length=500, blank=True, null=True)
    biography = models.TextField(blank=True)
    professional_affiliations = models.CharField(default='N/A',help_text=_("Enter your professional affiliations"), max_length=700, blank=True, null=True)
    identity_choice = models.CharField(help_text=_("Select your identity document"), max_length=100, choices=IdentityNumberChoices.choices, default=IdentityNumberChoices.ID_NUMBER)
    identity_number = models.CharField(unique=True, max_length=13, null=True, blank=True)
    verification_status = models.CharField(max_length=100, choices=StatusChoices.choices, default=StatusChoices.NOT_APPROVED)
    is_technical = models.BooleanField(default=False)
    is_email_activated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        ordering = ["-created"]

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        if self.title:
            return f"{self.title} {self.first_name[0]} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"
        
    def get_absolute_url(self):
        return reverse("accounts:user-details", kwargs={"username": self.username})
     
class IdentityVerification(AbstractCreate):
    identity_image =  models.ImageField(upload_to=handle_verification_docs_upload, null=False, help_text=_("Please take a selfie while holding an official identification document(ID Card, Passport)"))
    identitybook_image = models.ImageField(upload_to=handle_verification_docs_upload, null=False, help_text=_("Please take a picture of your official identification document(ID Card, Passport, drivers license, etc)"))
    user = models.OneToOneField(Account, related_name="verification", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Identity Verification")
        verbose_name_plural = _("Identity Verifications")
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("accounts:verify")
    
    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - Identity verification data"
