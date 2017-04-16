from django.conf.urls import include, url
from django.contrib import admin

from allauth.account.views import SignupView, LoginView, PasswordResetView

class MySignupView(SignupView):
    template_name = 'account/signup.html'

class MyLoginView(LoginView):
    template_name = 'account/login.html'

class MyPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset.html'


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login', MyLoginView.as_view(), name='account_login'),
    url(r'^accounts/signup', MySignupView.as_view(), name='account_signup'),
    url(r'^accounts/password_reset', MyPasswordResetView.as_view(), name='account_reset_password'),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^classifieds/', include('classified.urls', namespace='classified')),
    url(r'^directory/', include('directory.urls',  namespace='directory')),
    url(r'^', include('homepage.urls')),
]
