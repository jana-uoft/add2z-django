from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^listings/$', views.listings, name='all-listings'),
    url(r'^listings/(?P<listing_id>[0-9]+)/$', views.listing, name='single-listing'),
    url(r'^listings/(?P<filters>[a-zA-Z0-9 =_&]+)$', views.listings, name='filter-listings'),
]



