from django import forms
from campaigns.models import CampaignModel, ContributionModel, CampaignUpdateModel
from tinymce.widgets import TinyMCE

class CampaignForm(forms.ModelForm):
    class Meta:
        model = CampaignModel
        fields = ("category", "title", "details", "target", "start_date", "end_date", "image", "small_description")
        widgets = {
            'small_description': forms.Textarea(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'title': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g John Snow's 30th Birthday"}),
            'target': forms.NumberInput(attrs={"step": "0.01", "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'category': forms.Select(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'image': forms.FileInput(attrs={"class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"}),
            'details': TinyMCE(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8}),
            'start_date': forms.DateTimeInput(attrs={"type": "text", "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "step": "any"}),
            'end_date': forms.DateTimeInput(attrs={"type": "text", "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "step": "any"})
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and start_date == end_date:
            raise forms.ValidationError("Campaign start and end times cannot be the same.")
        
        if end_date.date() < start_date.date():
            raise forms.ValidationError("Start date cannot be greater than end date")
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.initial.items():
            if field_value is None:
                self.initial[field_name] = ''

class CampaignAddressForm(forms.ModelForm):
    class Meta:
        model = CampaignModel
        fields = ("campaign_address", "map_coordinates")

        widgets = {
            'map_coordinates': forms.HiddenInput(),
            'campaign_address': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g Durban St, Durban, 4312, KZN"}),
            }


class CampaignContactForm(forms.ModelForm):
    class Meta:
        model = CampaignModel
        fields = ("facebook", "twitter", "instagram", "linkedIn", "phone", "website", "email", "alternative_phone")

        widgets = {
            'phone': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g Durban St, Durban, 4312, KZN"}),
            'website': forms.URLInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g https://www.business.co.za"}),
            'email': forms.EmailInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g info@business.co.za"}),
            }      

class ContributionForm(forms.ModelForm):
    class Meta:
        model = ContributionModel
        fields = ("amount", "tip", "anonymous", "accepted_laws", "message")

class CampaignUpdateForm(forms.ModelForm):
    class Meta:
        model = CampaignUpdateModel
        fields = ("title", "content")

        widgets = {
            'title': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g John Snow's 30th Birthday"}),
            }