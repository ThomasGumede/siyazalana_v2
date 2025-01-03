from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

urlpatterns = [
    path('siyazalana_admin/', admin.site.urls),
    path("", include("siyazalana_home.urls", namespace="siyazalana_home")),
    path("", include("accounts.urls", namespace="accounts")),
    path("", include("campaigns.urls", namespace="campaigns")),
    path("", include("events.urls", namespace="events")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
