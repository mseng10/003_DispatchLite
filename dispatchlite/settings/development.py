from dispatchlite.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j04#7k2y*#1y%)54it3h1ve^2#iafyq-%^d$6sw1ceg58j-m!h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres2',
        'USER': 'postgres',
        'PASSWORD': 'PG123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['*']
