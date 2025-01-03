import uuid
from django.db import models
from django.utils.translation import gettext as _
from accounts.utilities.validators import validate_fcbk_link, validate_in_link, validate_insta_link, validate_twitter_link, verify_rsa_phone

PHONE_VALIDATOR = verify_rsa_phone()

PROVINCES = [
    ("kzn", "KwaZulu-Natal"),
    ("mp", "Mpumalanga"),
    ("nw", "North-West"),
    ("fs", "Free-State"),
    ("wc", "Western Cape"),
    ("lp", "Limpopo"),
    ("gp", "Gauteng"),
    ("ec", "Eastern Cape"),
    ("nc", "Northern Cape"),
]

class AbstractProfile(models.Model):
    address_one = models.CharField(max_length=300, blank=True, null=True)
    address_two = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=300, blank=True, null=True)
    province = models.CharField(max_length=300, blank=True, null=True, choices=PROVINCES)
    country = models.CharField(max_length=300, default="South Africa")
    zipcode = models.BigIntegerField(blank=True, null=True)
    address_id = models.CharField(max_length=300, null=True, blank=True)

    phone = models.CharField(help_text=_("Enter cellphone number"), max_length=15, validators=[PHONE_VALIDATOR], unique=True, null=True, blank=True)
    facebook = models.URLField(validators=[validate_fcbk_link], blank=True, null=True)
    twitter = models.URLField(validators=[validate_twitter_link], blank=True, null=True)
    instagram = models.URLField(validators=[validate_insta_link], blank=True, null=True)
    linkedIn = models.URLField(validators=[validate_in_link], blank=True, null=True)

    class Meta:
        abstract = True
        
    



class AbstractCreate(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AbstractPayment(models.Model):
    payment_method_type = models.CharField(max_length=50, null=True, blank=True)
    payment_method_card_holder = models.CharField(max_length=50, null=True, blank=True)
    payment_method_masked_card = models.CharField(max_length=50, null=True, blank=True)
    payment_method_scheme = models.CharField(max_length=50, null=True, blank=True)
    payment_date = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True