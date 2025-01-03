from django.urls import path
from siyazalana_home.views.admin_views import all_accounts
from siyazalana_home.views.blog_views import all_blogs, blog_details, blogs, create_blog, delete_blog, update_blog
from siyazalana_home.views.campaigns_views import all_campaigns, all_contributions, campaign_details, contribution_details, delete_contribution
from siyazalana_home.views.events_views import all_events, all_ticket_orders, delete_ticket_order, event_details, ticket_order_details
from siyazalana_home.views.home import about_siyazalana, contact, dashboard, faqs, home, privacy, refunds, search, terms_and_conditions
from siyazalana_home.views.member_views import create_member, delete_member, team_member_details, team_members, update_member

app_name = 'siyazalana_home'
urlpatterns = [
    path("", home, name="siyazalana-home"),
    path("about-us", about_siyazalana, name="about-siyazalana"),
    path("about-us/teams/<member_id>", team_member_details, name="team-member"),
    path("contact-us", contact, name="contact"),
    path("dashboard", dashboard, name="dashboard"),
    path("search", search, name="search"),
    path("siyazalana/faqs", faqs, name="faqs"),
    path("about-us/privacy", privacy, name="policy"),
    path("about-us/refund-policy", refunds, name="refund"),
    path("about-us/terms-and-conditions", terms_and_conditions, name="terms"),
    path("blogs", blogs, name="blogs"),
    path("blogs/<slug:category_slug>", blogs, name="blogs-by-category"),
    path("dashboard/accounts", all_accounts, name="all-accounts"),
    path("dashboard/blogs", all_blogs, name="all-blogs"),
    path("dashboard/blogs/create", create_blog, name="create-blog"),
    path("blogs/details/<slug:post_slug>", blog_details, name="details-blog"),
    path("dashboard/blogs/update/<slug:post_slug>", update_blog, name="update-blog"),
    path("dashboard/blogs/delete/<slug:post_slug>", delete_blog, name="delete-blog"),

    path("dashboard/members", team_members, name="team-members"),
    path("dashboard/member/create", create_member, name="create-member"),
    path("dashboard/member/update/<member_id>", update_member, name="update-member"),
    path("dashboard/member/delete/<member_id>", delete_member, name="delete-member"),
    path("dashboard/campaigns", all_campaigns, name="all-campaigns"),
    path("dashboard/campaign/<slug:campaign_slug>", campaign_details, name="campaign-details"),
    path("dashboard/accounts/campaigns/<username>", all_campaigns, name="all-campaigns-by-username"),
    path("dashboard/events", all_events, name="all-events"),
    path("dashboard/event/<slug:event_slug>", event_details, name="event-details"),
    path("dashboard/accounts/events/<username>", all_events, name="all-events-by-username"),
    path("dashboard/contributions", all_contributions, name="all-contributions"),
    path("dashboard/contributions/<contribution_id>", contribution_details, name="contribution"),
    path("dashboard/contribution/delete/<uuid:contribution_id>", delete_contribution, name="delete-contribution"),
    path("dashboard/ticket-orders", all_ticket_orders, name="all-ticket-orders"),
    path("dashboard/ticket-orders/<order_id>", ticket_order_details, name="order"),
    path("dashboard/ticket-orders/delete/<uuid:order_id>", delete_ticket_order, name="cancel-ticket-order"),
]
