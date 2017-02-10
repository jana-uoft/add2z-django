from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^listings/$', views.listings, name='listings'),
    url(r'^listings/(?P<listing_id>[0-9]+)/$', views.listing, name='listing'),
]
