"""
Development specific settings.
"""

from core.settings.base import *
from decouple import config

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'core',
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
