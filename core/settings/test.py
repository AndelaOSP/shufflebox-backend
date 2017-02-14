"""
Test specific settings.
"""

from core.settings.base import *

#Use the following live settings to build on Travis CI
if os.getenv('TRAVIS_BUILD', None):
    SECRET_KEY = os.getenv('SECRET_KEY')
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
