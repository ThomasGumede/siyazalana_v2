from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from .sitemaps import StaticViewSitemap, CampaignSitemap, EventSitemap, BlogSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'campaigns': CampaignSitemap,
    'events': EventSitemap,
    'blogs': BlogSitemap
}
urlpatterns = [
    path('siyazalana_admin/', admin.site.urls),
    path("", include("siyazalana_home.urls", namespace="siyazalana_home")),
    path("", include("accounts.urls", namespace="accounts")),
    path("", include("campaigns.urls", namespace="campaigns")),
    path("", include("events.urls", namespace="events")),
    path("payments/", include("payments.urls", namespace="payments")),
    path("coupons/", include("coupons.urls", namespace="coupons")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

urlpatterns += [path('i18n/', include('django.conf.urls.i18n')),]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

