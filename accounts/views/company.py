from accounts.models import AboutCompany
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# forms
class CompanyAddressForm(forms.ModelForm):
    class Meta:
        model = AboutCompany
        fields = ("address_one", "city", "province", "address_two", "zipcode", "email", "phone", "linkedIn", "facebook", "twitter", "instagram", "small_description", "slogan", "title", "vision", "mission")
        widgets = {
            'vision': forms.Textarea(attrs={"class": "!min-h-[50px] text-custom-text pl-5 pr-[50px] py-[15px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8, "placeholder": "Company Vision"}),
            'mission': forms.Textarea(attrs={"class": "!min-h-[50px] text-custom-text pl-5 pr-[50px] py-[15px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8, "placeholder": "Company Mission"}),
            'address_one': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'address_two': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'city': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'country': forms.TextInput(attrs={"value": "South Africa", "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'province': forms.Select(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'zipcode': forms.NumberInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"})
        }
@login_required
def update_company_address(request):
    company = get_object_or_404(AboutCompany, slug="about-siyazalana-model")
    form = CompanyAddressForm(instance=company)
    if request.method == "POST":
        form = CompanyAddressForm(instance=company, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Company details updated successfully")
            return redirect("accounts:update-company-details")
        else:
            messages.error(request, "Please fix errors below")
            return render(request, "accounts/company/update-address.html", {"form": form, "company": company})
    return render(request, "accounts/company/update-address.html", {"form": form, "company": company})
