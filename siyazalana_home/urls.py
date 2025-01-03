from django.urls import path

from siyazalana_home.views.home import home

app_name = 'siyazalana_home'
urlpatterns = [
    path("", home, name="siyazalana-home")
]
