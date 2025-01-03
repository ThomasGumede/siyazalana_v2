from django.urls import path
from accounts.views.account import account_update, activate, activation_sent, confirm_email, custom_login, custom_logout, general, register
from accounts.views.password import password_change, password_reset_request, password_reset_sent, passwordResetConfirm

app_name = "accounts"

urlpatterns = [
    path("account/login", custom_login, name="login"),
    path("account/logout", custom_logout, name="logout"),
    path("account/get-started", register, name="register"),
    path('account/get-started/success', activation_sent, name='success'),
    path('account/get-started/activate/<uidb64>/<token>', activate, name='activate'),
    path('account/confirm/email/<uidb64>/<token>', confirm_email, name='confirm-email'),
    path("account/password/reset", password_reset_request, name="password-reset"),
    path('account/password/success', password_reset_sent, name='password-reset-sent'),
    path('account/password/reset/<uidb64>/<token>', passwordResetConfirm, name='password-reset-confirm'),
    
    path('account/manage/update-profile', account_update, name="profile-update"),
    path('account/manage/update-contact', general, name="contact-update"),
    path('account/manage/update-password', password_change, name="password-update"),
    # path('dashboard/update/social', add_social_links, name="update-social-links"),

]

