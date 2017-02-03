"""
Test specific settings.
"""

from shufflebox.settings.base import *

#Use the following live settings to build on Travis CI
if os.getenv('TRAVIS_BUILD', None):
    SECRET_KEY = "SecretKeyForUseOnTravis"
    DEBUG = False
    TEMPLATE_DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travis_ci_db',
            'USER': 'travis',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
        }
    }
