from django.contrib import admin
from payments.models import SiyazalanaBank, PaymentInformation

@admin.register(SiyazalanaBank)
class SiyazalanaBankBankAdmin(admin.ModelAdmin):
    pass

@admin.register(PaymentInformation)
class PaymentInformation(admin.ModelAdmin):
    pass
    
