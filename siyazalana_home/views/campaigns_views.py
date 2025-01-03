from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from siyazalana_home.forms import CampaignUpdateStatusForm
from siyazalana_home.utilities.decorators import user_not_superuser_or_staff
from campaigns.models import CampaignModel, ContributionModel
from django.contrib import messages

from campaigns.utils import PaymentStatus

USER = get_user_model()

@login_required
@user_not_superuser_or_staff
def all_campaigns(request, username=None):
    query = request.GET.get("query", None)
    queryset = CampaignModel.objects.all()
    if username:
        user = get_object_or_404(USER, username=username)
        if query:
            campaigns = queryset.filter(Q(organiser = user) & Q(title__icontains=query)| Q(organiser__first_name__icontains=query))
        else:
            campaigns = queryset.filter(organiser = user)
    else:
        if query:
            campaigns = queryset.filter(Q(title__icontains=query)| Q(organiser__first_name__icontains=query))
        else:
            campaigns = queryset
    
    return render(request, "dashboard/campaigns/all-campaigns.html", {"campaigns": campaigns, "query": query})

@login_required
@user_not_superuser_or_staff
def campaign_details(request, campaign_slug):
    
    queryset = CampaignModel.objects.select_related("organiser", "category").prefetch_related("contributions").order_by("-created")
    campaign = get_object_or_404(queryset, slug = campaign_slug)
    backers = campaign.contributions.filter(paid="PAID").count()
    form = CampaignUpdateStatusForm(instance=campaign)

    if request.method == "POST":
        form = CampaignUpdateStatusForm(instance=campaign, data=request.POST)
        if form.is_valid():
            campaign = form.save()
            messages.success(request, "Campaign status was changed successfully")
            return redirect("siyazalana_home:campaign-details", campaign_slug=campaign.slug)
    

    return render(request, "dashboard/campaigns/campaign-details.html", {"campaign": campaign, "form": form, "backers": backers})

@login_required
@user_not_superuser_or_staff
def all_contributions(request, campaign_id = None):
    
    contributions = ContributionModel.objects.select_related("contributor").all()
    campaign_model = None

    if campaign_id:
        campaign_model = get_object_or_404(CampaignModel, id=campaign_id)
        contributions = ContributionModel.objects.filter(campaign = campaign_model).select_related("contributor")
        

    return render(request, "dashboard/contributions/contributions.html", {"orders": contributions, "campaign": campaign_model})

@login_required
@user_not_superuser_or_staff
def contribution_details(request, contribution_id):
    contributions = ContributionModel.objects.all().select_related("contributor")
    contribution = get_object_or_404(contributions, id=contribution_id)
    return render(request, "dashboard/contributions/details.html", {"order": contribution})

@login_required
@user_not_superuser_or_staff
def delete_contribution(request, contribution_id):
    contribution = get_object_or_404(ContributionModel, id = contribution_id)
    if contribution.paid == PaymentStatus.PAID:
        messages.warning(request, "You cannot delete already paid payment contribution, please visit our <a href='' class='text-custom-primary'>refund policy</a>")
        return redirect("siyazalana_home:all-contributions")
    
    if request.method == "POST":
        contribution.delete()
        messages.success(request, "You contribution was deleted successfully")
        return redirect("siyazalana_home:all-contributions")
    
    return render(request, "campaigns/delete/confirm_delete.html", {"message": f"Are you sure you want to cancel this contribution ({contribution.order_number})?", "title": "Cancel Contribution"})
