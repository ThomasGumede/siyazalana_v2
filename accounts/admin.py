from django.contrib import admin
from accounts.models import Account, AboutCompany

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(AboutCompany)
class AboutCompanyAdmin(admin.ModelAdmin):
    pass
