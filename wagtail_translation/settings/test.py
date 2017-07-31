from .base import *  # NOQA

DEBUG = False

DATABASES = {
    'default': {
        'NAME': 'test.sqlite',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS += (
    'wagtail_translation.tests',
)

ROOT_URLCONF = 'wagtail_translation.tests.urls'
WAGTAIL_SITE_NAME = 'Wagtail Translation Test'