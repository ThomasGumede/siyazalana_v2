from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm,  UserCreationForm)

from accounts.utilities.choices import IdentityNumberChoices
from accounts.utilities.validators import validate_sa_id_number, validate_sa_passport_number

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username or Email', 'id': 'id_username'}), label="Username or Email*")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'id_password'}))

class RegistrationForm(UserCreationForm):
    confirm_email = forms.EmailField(help_text="Confirm your email address", required=True, widget=forms.EmailInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}))

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            'email': forms.EmailInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            'confirm_email': forms.EmailInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            'first_name': forms.TextInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            'last_name': forms.TextInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            #'hobbies': forms.TextInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            'password1': forms.PasswordInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            'password2': forms.PasswordInput(attrs={"class": "w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"}),
            
        }

    def clean_email(self):
        email = self.cleaned_data["email"]

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(f'This email: {email} is already in use.')
        
        return email
    
    def clean(self):
        clean = super().clean()
        second_email = clean.get("confirm_email", None)
        mail = clean.get("email", None)

        if second_email and mail and mail != second_email:
            raise forms.ValidationError(f'This email: {mail} does not match with confirmation email.')
        
        

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()

        return user

class AccountUpdateForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = ["title", "profile_image", "first_name", "last_name", 'maiden_name', "biography", "identity_choice", "identity_number"]

        widgets = {
            'username': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'title': forms.Select(attrs={"class": "block p-3 md:text-base w-full text-sm text-custom-h outline-none placeholder:text-gray-400 bg-gray-50 rounded-lg border border-gray-300 focus:ring-custom-primary focus:border-custom-primary ease-linear transition-all duration-150"}),
            'first_name': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'maiden_name': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'last_name': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            #'hobbies': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            
        }

    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.initial.items():
            if field_value is None:
                self.initial[field_name] = ''
                
    def clean(self):
        clean = super().clean()
        identity_choice = clean.get('identity_choice', None)
        identity_number = clean.get('identity_number', None)

        if identity_number and identity_choice:
            if identity_choice == IdentityNumberChoices.ID_NUMBER:
                message = validate_sa_id_number(identity_number)
                if message["success"] == False:
                    raise forms.ValidationError(message["message"])
            else:
                if not validate_sa_passport_number(identity_number):
                    raise forms.ValidationError("Your passport number is invalid")
            
        return clean
     
class GeneralEditForm(forms.ModelForm):
    """
        Form to edit only username and email
    """
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "phone", "address_one", "address_two", "city", "country", "province", "zipcode"]

        widgets = {
            'address_one': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'address_two': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'city': forms.TextInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'country': forms.TextInput(attrs={"value": "South Africa", "class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'province': forms.Select(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"}),
            'zipcode': forms.NumberInput(attrs={"class": "text-custom-text pl-5 pr-[50px] outline-none border-2 border-[#e4ecf2] focus:border focus:border-custom-primary h-[65px] block w-full rounded-none focus:ring-0 focus:outline-none placeholder:text-custom-text placeholder:text-sm"})
        }

    def __init__(self, *args, **kwargs):
        super(GeneralEditForm, self).__init__(*args, **kwargs)
        for field_name, field_value in self.initial.items():
            if field_value is None:
                self.initial[field_name] = ''

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get("email")
        if get_user_model().objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(f'This username: {username} is already in use.')
        
        if get_user_model().objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(f'This email: {email} is already in use.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super(GeneralEditForm, self).save(commit=False)
        email = self.cleaned_data['email']
        if commit:
            user.save()
            
        return user

class SocialLinksForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("facebook", "twitter", "instagram", "linkedIn")

        