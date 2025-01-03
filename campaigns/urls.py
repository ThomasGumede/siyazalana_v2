from django.urls import path 
from campaigns.views.campaign import (campaigns, campaign_details, create_campaign_address, add_campaign_socials, update_campaign_address, update_campaign_contact,
                                      create_campaign, update_campaign, delete_campaign, manage_campaigns, manage_campaign, generate_contributors_list)
from campaigns.views.contribution import (
    create_contribution, cancel_contribution, contribution, contributions, manage_contribution, manage_contributions, get_contributors
)
from campaigns.views.campaign_update import create_campaign_update, delete_campaign_update

app_name = "campaigns"
urlpatterns = [
    path("campaigns", campaigns, name="campaigns"),
    path("account/campaigns/manage", manage_campaigns, name="manage-campaigns"),
    path("campaign/get-started", create_campaign, name="create-campaign"),
    path("campaign/get-started/<slug:campaign_slug>", create_campaign, name="create-campaign-with-slug"),
    path("campaign/add-address/<slug:campaign_slug>", create_campaign_address, name="create-campaign-address"),
    path("campaign/add-contact/<slug:campaign_slug>", add_campaign_socials, name="create-campaign-contact"),
    path("<slug:category_slug>", campaigns, name="campaign-by-category"),
    path("campaing/<slug:campaign_slug>", campaign_details, name="campaign"),
    path("campaign/manage/<uuid:campaign_id>", manage_campaign, name="manage-campaign"),
    path("campaign/contributors/manage/<uuid:campaign_id>", get_contributors, name="get-contributors"),
    path("campaign/manage/update-details/<slug:campaign_slug>", update_campaign, name="update-campaign"),
    path("campaign/manage/update-address/<slug:campaign_slug>", update_campaign_address, name="update-campaign-address"),
    path("campaign/manage/update-contact/<slug:campaign_slug>", update_campaign_contact, name="update-campaign-contact"),
    path("campaign/manage/delete/<slug:campaign_slug>", delete_campaign, name="delete-campaign"),

    path("campaign/manage/updates/create/<slug:campaign_slug>", create_campaign_update, name="create-campaign-update"),
    path("campaign/manage/updates/delete/<uuid:update_id>", delete_campaign_update, name="delete-campaign-update"),

    path("campaign/manage/contributions/all", contributions, name="all-contributions"),
    path("campaign/manage/contributions/all/<uuid:campaign_id>", contributions, name="contributions"),
    path("account/contributions/manage", manage_contributions, name="manage-contributions"),
    path("campaign/manage/contribution/<uuid:campaign_id>/<uuid:contribution_id>", contribution, name="contribution"),
    path("account/contributions/manage/<uuid:contribution_id>", manage_contribution, name="manage-contribution"),
    path("contribution/create/<uuid:campaign_id>", create_contribution, name="create-contribution"),
    path("contribution/cancel/<uuid:contribution_id>", cancel_contribution, name="cancel-contribution"),
    path("contribution/generate/contributors/<uuid:campaign_id>", generate_contributors_list, name="generate-contributors-list")
    
]
