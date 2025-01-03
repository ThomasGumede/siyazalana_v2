import logging
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from siyazalana_home.utilities.decorators import user_not_superuser_or_staff
from django.contrib.auth import get_user_model
from django.db.models import Q

USER = get_user_model()

@login_required
@user_not_superuser_or_staff
def all_accounts(request):
    template = "dashboard/accounts/users.html"
    query = request.GET.get("q", None)
    users = USER.objects.all()
    if query:
        users = USER.objects.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query) 
            | Q(address_one__icontains = query)
        )
        
    return render(request, "dashboard/accounts/all-accounts.html", {"accounts": users, "query": query})


