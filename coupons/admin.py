from django.contrib import admin
from coupons.models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass
