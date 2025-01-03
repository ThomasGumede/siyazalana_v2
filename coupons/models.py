from django.db import models
from accounts.custom_models.abstracts import AbstractCreate


class Coupon(AbstractCreate):
    discount = models.DecimalField(max_digits=1000, decimal_places=2)
    code = models.CharField(max_length=50, unique=True)
    order_id = models.UUIDField(unique=True, null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField()

    def __str__(self) -> str:
        return self.code
    
    def get_formated_date(self):
        return