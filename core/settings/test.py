"""
Test specific settings.
"""

from core.settings.base import *
from decouple import config

#Use the following live settings to build on Travis CI
if config('TRAVIS_BUILD', default=None):
    SECRET_KEY = config('SECRET_KEY')
    DEBUG = False

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travis_ci_db',
            'USER': 'travis',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
        }
    }
