from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from campaigns.models import CampaignModel, ContributionModel
from campaigns.utils import PaymentStatus, generate_slug
from campaigns.forms import CampaignContactForm, CampaignForm, CampaignAddressForm
from accounts.custom_models.choices import StatusChoices
from siyazalana_home.models import BlogCategory
from django.contrib import messages
from django.db.models import Q
from weasyprint import HTML
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.db.models import Prefetch
import logging

logger = logging.getLogger("campaigns")

@login_required
def manage_campaigns(request):
    campaigns = CampaignModel.objects.filter(organiser = request.user)
    return render(request, "campaigns/campaign/manage/campaigns.html", {"campaigns": campaigns})


@login_required
def generate_contributors_list(request, campaign_id):
    quertset = CampaignModel.objects.prefetch_related(Prefetch("contributions", queryset=ContributionModel.objects.filter(paid=PaymentStatus.PAID)))
    campaign = get_object_or_404(quertset, organiser = request.user, id=campaign_id)
    domain = get_current_site(request).domain

    protocol = "https" if request.is_secure() else "http"
    if campaign.contributions.count() < 1:
        messages.warning(request, "Sorry You cannot generate contributors list for now")
        return redirect("campaigns:manage-campaign", campaign_id=campaign.id)
    
    try:
        template = get_template("list/contributors.html")
        context = { 
                    "campaign": campaign,
                    "domain": domain, 
                    "protocol": protocol}
        
        render_template = template.render(context)
        pdf_file = HTML(string=render_template).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{campaign.title}_Contributors_List.pdf"'

        return response
    
    except Exception as ex:
        logger.error(ex)
        messages.error(request, "Sorry there was an error trying to generate your Contributors list")
        return redirect("campaigns:manage-campaign", campaign_id=campaign.id)

@login_required
def manage_campaign(request, campaign_id):
    try:
        campaign = get_object_or_404(CampaignModel.objects.prefetch_related("contributions").all(), organiser = request.user, id=campaign_id)
        amount = sum([contribution.amount for contribution in campaign.contributions.filter(paid = PaymentStatus.PAID)])
        return render(request, "campaigns/campaign/manage/campaign.html", {"campaign": campaign, "sales": amount})
    
    except CampaignModel.MultipleObjectsReturned:
        logger.error("Something went wrong")
        messages.error(request, f"Something went wrong, we are trying to fix it")
        return redirect("campaigns:manage-campaigns")

def campaigns(request, category_slug=None):
    query = request.GET.get("query", None)
    queryset = CampaignModel.objects.filter(Q(status = StatusChoices.APPROVED) | Q(status = StatusChoices.COMPLETED))
    if category_slug:
        category = get_object_or_404(BlogCategory, slug=category_slug)
        if query:
            campaigns = queryset.filter(Q(category = category) & Q(title__icontains=query)| Q(organiser__first_name__icontains=query))
        else:
            campaigns = queryset.filter(category = category)
    else:
        if query:
            campaigns = queryset.filter(Q(title__icontains=query)| Q(organiser__first_name__icontains=query))
        else:
            campaigns = queryset
    
    return render(request, "campaigns/campaign/list.html", {"campaigns": campaigns, "query": query})

def campaign_details(request, campaign_slug):
    queryset = CampaignModel.objects.select_related("organiser", "category").order_by("-created")
    campaign = get_object_or_404(queryset, slug = campaign_slug)
    recent_campaigns = queryset[:5]

    return render(request, "campaigns/campaign/details.html", {"campaign": campaign, "recent_campaigns":recent_campaigns})

@login_required
def create_campaign(request, campaign_slug=None):
    campaign=None
    if campaign_slug:
        campaign = get_object_or_404(CampaignModel, slug=campaign_slug, organiser=request.user)
        
    form = CampaignForm(instance=campaign)
    if request.method == 'POST':
        form = CampaignForm(instance=campaign, data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            campaign = form.save(commit=False)
            campaign.slug = generate_slug(campaign.title, CampaignModel)
            campaign.organiser = request.user
            campaign.save()
            messages.success(request, "Campaign was created successfully. Add address now")
            return redirect("campaigns:create-campaign-address", campaign_slug=campaign.slug)
        else:
            messages.error(request, "Failed to Add Campaign, please fix errors below")
    
    return render(request, "campaigns/campaign/create/campaign-details.html", {"form": form, "campaign": campaign})

@login_required
def create_campaign_address(request, campaign_slug):
    campaign = get_object_or_404(CampaignModel, slug=campaign_slug, organiser=request.user)
    form = CampaignAddressForm(instance=campaign)
    if request.method == 'POST':
        form = CampaignAddressForm(instance=campaign, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Campaign address added successfully")
            return redirect("campaigns:create-campaign-contact", campaign_slug=campaign.slug)
            
    return render(request, "campaigns/campaign/create/campaign-location.html", {"form": form, "campaign": campaign})

@login_required
def add_campaign_socials(request, campaign_slug):
    campaign = get_object_or_404(CampaignModel, slug=campaign_slug, organiser=request.user)
    form = CampaignContactForm(instance=campaign)
    
    if request.method == "POST":
        form = CampaignContactForm(instance=campaign, data=request.POST)

        if form.is_valid():
            form.save()
            # send_html_email('New campaign Added', 'campaigns@bbgi.co.za', 'emails/campaign-confirmation.html', {"campaign": campaign})
            messages.success(request, "campaign contact details successfully added. It takes 12 - 48 hours for campaign status to be updated, will contact you if we require additional information. Thank you")
            return redirect("campaigns:manage-campaign", campaign_id=campaign.id)
        else:
            messages.error(request, "Something went wrong while trying to add your business")
            return render(request, "campaigns/campaign/create/campaign-contact.html", {"campaign": campaign, "form": form})
    
    return render(request, "campaigns/campaign/create/campaign-contact.html", {"campaign": campaign, "form": form})


@login_required
def update_campaign(request, campaign_slug):
    try:
        campaign = get_object_or_404(CampaignModel, organiser = request.user, slug = campaign_slug)
        if campaign.status in [StatusChoices.APPROVED, StatusChoices.PENDING]:
            messages.error(request, "You cannot edit campaign that is already approved or pending approval")
            return redirect("campaigns:manage-campaigns")
        form = CampaignForm(instance=campaign)
        if request.method == 'POST':
            form = CampaignForm(instance=campaign,data=request.POST, files=request.FILES)
            if form.is_valid() and form.is_multipart():
                campaign = form.save(commit=False)
                campaign.save()
                messages.success(request, "Campaign was updated successfully")
                
            else:
                messages.error(request, "Error trying to update campaign, fix issues below")
        
        
        return render(request, "campaigns/campaign/update.html", {"form": form, "campaign": campaign})
    
    except CampaignModel.MultipleObjectsReturned:
        logger.error("Something went wrong")
        CampaignModel.objects.filter(organiser=request.user, slug=campaign_slug).first().delete()
        messages.error(request, f"Something went wrong, it looks like you save two campaigns with the same title... will fix it")
        return redirect("campaigns:manage-campaigns")
    
@login_required
def update_campaign_address(request, campaign_slug):
    campaign = get_object_or_404(CampaignModel, slug=campaign_slug, organiser=request.user)
    form = CampaignAddressForm(instance=campaign)
    if request.method == 'POST':
        form = CampaignAddressForm(instance=campaign, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Campaign address added successfully")
            
    return render(request, "campaigns/campaign/update/campaign-location.html", {"form": form, "campaign": campaign})

@login_required
def update_campaign_contact(request, campaign_slug):
    campaign = get_object_or_404(CampaignModel, slug=campaign_slug, organiser=request.user)
    form = CampaignContactForm(instance=campaign)
    
    if request.method == "POST":
        form = CampaignContactForm(instance=campaign, data=request.POST)

        if form.is_valid():
            form.save()
            # send_html_email('New campaign Added', 'campaigns@bbgi.co.za', 'emails/campaign-confirmation.html', {"campaign": campaign})
            messages.success(request, "campaign contact details successfully updated.")
            
        else:
            messages.error(request, "Something went wrong while trying to add your business")

    return render(request, "campaigns/campaign/update/campaign-contact.html", {"campaign": campaign, "form": form}) 

@login_required
def delete_campaign(request, campaign_slug):
    campaign = get_object_or_404(CampaignModel.objects.prefetch_related("contributions"), organiser = request.user, slug = campaign_slug)
    if campaign.contributions.filter(Q(paid = PaymentStatus.PENDING)| Q(paid = PaymentStatus.PAID)).count() > 0:
        messages.warning(request, "You cannot delete this campaign, there are pending or paid contributions in this campaign")
        return redirect("campaigns:manage-campaigns")
    if request.method == "POST":
        campaign.delete()
        return redirect("campaigns:manage-campaigns")
    
    return render(request, "campaigns/delete/confirm_delete.html", {"message": f"Are you sure you want to delete this campaign ({campaign.title})?", "title": "Delete campaign"})
