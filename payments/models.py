import uuid
from django.db import models
from accounts.models import AbstractCreate

class SiyazalanaBank(AbstractCreate):
    balance = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    order_uuid = models.UUIDField(null=True, blank=True)
    order_id = models.CharField(max_length=300)
    tip = models.CharField(max_length=200, null=True, blank=True)
    received_at = models.DateTimeField(auto_now_add=True)

# celery -A BBGIfam worker/beat -l info
    def __str__(self) -> str:
        return f"{self.order_id} - {self.received_at}"
    
    class Meta:
        verbose_name = 'BBGI Finance Information'
        verbose_name_plural = 'BBGI Finance Informations'
        ordering = ["-created"]

class PaymentInformation(models.Model):
    id = models.CharField(max_length=300, unique=True, primary_key=True, db_index=True, editable=False)
    data = models.JSONField()
    order_number = models.CharField(max_length=300, editable=False, null=True, blank=True)
    order_updated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.order_number} - {self.created}"
    
    class Meta:
        verbose_name = 'Payment Information'
        verbose_name_plural = 'Payment Informations'
        ordering = ["-created"]