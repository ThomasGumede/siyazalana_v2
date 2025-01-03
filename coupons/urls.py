from django.urls import path
from coupons.views import apply_coupon

app_name = "coupons"
urlpatterns = [
    path("coupon/apply-coupon", apply_coupon, name="apply-coupon")
]

