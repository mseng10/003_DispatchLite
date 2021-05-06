from dispatchlite.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j04#7k2y*#1y%)54it3h1ve^2#iafyq-%^d$6sw1ceg58j-m!h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres1',
        'USER': 'postgres',
        'PASSWORD': 'temppassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
EMAIL_PORT = 587
EMAIL_USE_TLS = True