from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^classifieds/', include('classified.urls', namespace='classified')),
    url(r'^directory/', include('directory.urls',  namespace='directory')),
    url(r'^', include('homepage.urls')),
]
