from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from siyazalana_home.models import Blog
from campaigns.models import CampaignModel  # Adjust based on your models
from events.models import EventModel  # Adjust based on your models

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return [
            'siyazalana_home:siyazalana-home',
            'siyazalana_home:about-siyazalana',
            'siyazalana_home:contact',
            'siyazalana_home:blogs',
            'campaigns:campaigns',
            'events:events'
        ]

    def location(self, item):
        return reverse(item)

class CampaignSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return CampaignModel.objects.all()

    def location(self, obj):
        return reverse('campaigns:campaign', args=[obj.slug])

class EventSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return EventModel.objects.all()

    def location(self, obj):
        return reverse('events:event-details', args=[obj.slug])
 
class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return Blog.objects.all()

    def location(self, obj):
        return reverse('siyazalana_home:details-blog', args=[obj.slug])
