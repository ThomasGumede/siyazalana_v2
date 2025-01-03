from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from coupons.models import Coupon
from coupons.forms import CouponApplyForm, CreateCouponForm
from django.contrib import messages

def coupons(request):
    return render(request, "coupons/all-coupons.html", {"coupons": Coupon.objects.all()})

@require_POST
def apply_coupon(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        return_url = form.cleaned_data["return_url"]
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            messages.success(request, "Coupon successfully applied")
            request.session["coupon_id"] = str(coupon.id)
        except Coupon.DoesNotExist:
            messages.error(request, "Coupon either not valid or already used")
            request.session["coupon_id"] = None

    return redirect(return_url)

def create_coupon(request):
    form = CreateCouponForm()
