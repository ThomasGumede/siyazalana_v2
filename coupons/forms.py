from django import forms

from coupons.models import Coupon

class CouponApplyForm(forms.Form):
    code = forms.CharField()
    return_url = forms.CharField()
    
class CreateCouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ('discount', 'valid_from', 'valid_to')
        
        widgets = {
            'rating_value': forms.HiddenInput(),
            'discount': forms.NumberInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "Type your name..."}),
            'valid_from': forms.DateTimeInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "Type your email..."}),
            'valid_to': forms.DateTimeInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "Type your comment title..."}),
            
            'comment': forms.Textarea(attrs={"class": "!min-h-[50px] text-custom-text pl-5 pr-[50px] py-[15px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8, "placeholder": "Type your comment..."}),
        }