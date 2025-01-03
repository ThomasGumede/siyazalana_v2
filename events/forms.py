from django import forms
from events.models import EventModel, TicketOrderModel, EventTicketTypeModel, TicketModel, EventOrganisor, EventReview, EventContent
from tinymce.widgets import TinyMCE

class EventForm(forms.ModelForm):
    
    class Meta:
        model = EventModel
        fields = ("image", "title", "email", "phone", "category", "content", "small_description", "venue_name", "event_address", "map_coordinates", "event_startdate", "event_enddate", "event_link")

        widgets = {
            'title': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g John Snow's 30th Birthday"}),
            'category': forms.Select(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'image': forms.FileInput(attrs={"class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"}),
            'map_coordinates': forms.HiddenInput(),
            'small_description': forms.Textarea(attrs={"class": "!min-h-[50px] text-custom-text pl-5 pr-[50px] py-[15px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8, "placeholder": "Event Short Description"}),
            'phone': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "type": "tel"}),
            'email': forms.EmailInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'venue_name': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g John Snow Hall, Next to Asgard"}),
            'event_link': forms.URLInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g https://www.eventtitle.co.za"}),
            'event_address': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g Durban St, Durban, 4312, KZN"}),
            'event_startdate': forms.DateTimeInput(attrs={"type": "text", "step": "any", "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "yyyy-mm-dd h:m:s"}),
            'content': TinyMCE(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8}),
            'event_enddate': forms.DateTimeInput(attrs={"type": "text", "step": "any", "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "yyyy-mm-dd h:m:s"})
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.initial.items():
            if field_value is None:
                self.initial[field_name] = ''
            
  
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("event_startdate")
        end_date = cleaned_data.get("event_enddate")
        if start_date and end_date and start_date == end_date:
            raise forms.ValidationError("Event start and end times cannot be the same.")
        
        if end_date.date() < start_date.date():
            raise forms.ValidationError("Start date cannot be greater than end date")
        
        return cleaned_data

class EventCreateForm(forms.ModelForm):
    
    class Meta:
        model = EventModel
        fields = ("image", "title", "email", "phone", "category", "content", "small_description", "event_startdate", "event_enddate", "event_link")

        widgets = {
            'title': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g John Snow's 30th Birthday"}),
            'category': forms.Select(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'image': forms.FileInput(attrs={"class": "w-[0.1px] h-[0.1px] opacity-0 overflow-hidden absolute -z-[1]"}),
            'map_coordinates': forms.HiddenInput(),
            'phone': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "type": "tel"}),
            'email': forms.EmailInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'small_description': forms.Textarea(attrs={"class": "!min-h-[50px] text-custom-text pl-5 pr-[50px] py-[15px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8, "placeholder": "Event Short Description", "maxlength": 160}),
            'venue_name': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g John Snow Hall, Next to Asgard"}),
            'event_link': forms.URLInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g https://www.eventtitle.co.za"}),
            'event_address': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g Durban St, Durban, 4312, KZN"}),
            'event_startdate': forms.DateTimeInput(attrs={"type": "text", "step": "any", "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "yyyy-mm-dd h:m:s"}),
            'content': TinyMCE(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8}),
            'event_enddate': forms.DateTimeInput(attrs={"type": "text", "step": "any", "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "yyyy-mm-dd h:m:s"})
        }

    def __init__(self, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.initial.items():
            if field_value is None:
                self.initial[field_name] = ''
            
  
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("event_startdate")
        end_date = cleaned_data.get("event_enddate")
        if start_date and end_date and start_date == end_date:
            raise forms.ValidationError("Event start and end times cannot be the same.")
        
        if end_date.date() < start_date.date():
            raise forms.ValidationError("Start date cannot be greater than end date")
        
        return cleaned_data

class EventAddressForm(forms.ModelForm):
    class Meta:
        model = EventModel
        fields = ("venue_name", "event_address", "map_coordinates")

        widgets = {
            'map_coordinates': forms.HiddenInput(),
            'venue_name': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g John Snow Hall, Next to Asgard"}),
            'event_address': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "e.g Durban St, Durban, 4312, KZN"}),
            }

class EventOrganisorForm(forms.ModelForm):
    add_another = forms.CharField(max_length=100, required=False)
    class Meta:
        model = EventOrganisor
        fields = ("full_name", "organisor_phone_one", "organisor_email")

        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'type': 'text', 
                    'class': 'text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm'
                    }
                ),
            'organisor_phone_one': forms.TextInput(
                attrs={
                    'type': 'text', 
                    'class': 'text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm'
                    }
                ),
            'organisor_email': forms.EmailInput(
                attrs={
                    'type': 'email',
                    'class': 'text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm'
                    }
                ),
            
                        
        }
 
class EventTicketTypeForm(forms.ModelForm):
    add_another = forms.CharField(max_length=100, required=False)
    class Meta:
        model = EventTicketTypeModel
        fields = ("title", "available_seats", "price", "sale_start", "sale_end")

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'type': 'text',
                    'placeholder': 'e.g 1 Person + 2 Kids',
                    'class': 'text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm'
                    }
                ),
            'available_seats': forms.NumberInput(
                attrs={
                    'type': 'number',
                    'value': '5', 
                    'class': 'text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm'
                    }
                ),
            'price': forms.NumberInput(
                attrs={
                    'type': 'number',
                    'step': '0.01',
                    'class': 'text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm'
                    }
                ),
            
            'sale_start': forms.DateTimeInput(attrs={"type": "text", "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'sale_end': forms.DateTimeInput(attrs={"type": "text", "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            
        }

class EventReviewForm(forms.ModelForm):
    class Meta:
        model = EventReview
        fields = ("comment", "commenter_full_names", "commenter_email", "rating_value", "comment_title")

        widgets = {
            'rating_value': forms.HiddenInput(),
            'commenter_full_names': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "Type your name..."}),
            'commenter_email': forms.EmailInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "Type your email..."}),
            'comment_title': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "placeholder": "Type your comment title..."}),
            
            'comment': forms.Textarea(attrs={"class": "!min-h-[50px] text-custom-text pl-5 pr-[50px] py-[15px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm", "rows": 8, "placeholder": "Type your comment..."}),
        }

class EventTicketTypeUpdateForm(forms.ModelForm):
    class Meta:
        model = EventTicketTypeModel
        fields = ("title", "available_seats", "price")

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'type': 'text', 
                    'class': 'text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm'
                    }
                ),
            'available_seats': forms.NumberInput(
                attrs={
                    'type': 'number', 
                    'class': 'text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm'
                    }
                ),
            'price': forms.NumberInput(
                attrs={
                    'type': 'number',
                    'step': '0.01',
                    'class': 'text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm'
                    }
                ),   
        }

class TicketOrderForm(forms.ModelForm):
    class Meta:
        model = TicketOrderModel
        fields = ("accepted_laws", "email", "quantity", "total_price")

class TicketOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = TicketOrderModel
        fields = ("client_first_name", "client_last_name", "order_note", "client_phone", "client_email", "client_address_one", "client_address_two", "client_city", "client_zipcode", "client_province")

class TicketForm(forms.ModelForm):
    class Meta:
        model = TicketModel
        exclude=["id"]
        fields = ("quantity", "ticket_type", "guest_email", "guest_full_name")
