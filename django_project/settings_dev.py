"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open('/etc/django_secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'homepage',
    'directory',
    'classified',
    'django.contrib.sites',
    'storages',
)

SITE_ID = 2

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'django_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Canada/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# Allow Django from all hosts. This snippet is installed from
# /var/lib/digitalocean/allow_hosts.py

# import os
# import netifaces

# # Find out what the IP addresses are at run time
# # This is necessary because otherwise Gunicorn will reject the connections
# def ip_addresses():
#     ip_list = []
#     for interface in netifaces.interfaces():
#         addrs = netifaces.ifaddresses(interface)
#         for x in (netifaces.AF_INET, netifaces.AF_INET6):
#             if x in addrs:
#                 ip_list.append(addrs[x][0]['addr'])
#     return ip_list

# Discover our IP address
# ALLOWED_HOSTS+= ip_addresses()


DEFAULT_FILE_STORAGE = 'storages.backends.gs.GSBotoStorage'
GS_ACCESS_KEY_ID = 'GOOGX6435EWNWMOKV552'
GS_SECRET_ACCESS_KEY = 'bjX44UUmYPxvD/wO/HHr4bP0Ohwm11mIu6enL7HU'
GS_BUCKET_NAME = 'add2z'
# STATICFILES_STORAGE = 'storages.backends.gs.GSBotoStorage'

# STATIC_URL = 'https://storage.googleapis.com/add2z/'
# STATIC_ROOT = 'https://storage.googleapis.com/add2z/'

