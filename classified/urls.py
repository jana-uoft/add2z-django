from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^listings/$', views.listings, name='all-listings'),
    url(r'^listings/(?P<listing_id>[0-9]+)/$', views.listing, name='single-listing'),
    url(r'^listings/(?P<filters>[a-zA-Z0-9 =_&]+)/$', views.listings, name='filter-listings'),
    url(r'^listings/(?P<filters>[a-zA-Z0-9 =_&]+)/(?P<remove>[a-zA-Z0-9 =_&]+)$', views.removeFilter, name='remove-filter-listings'),

    url(r'^accounts/login/$', views.sign_in, name='sign_in'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^accounts/logout/$', views.sign_out, name='sign_out'),

]



