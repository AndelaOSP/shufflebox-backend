"""
Settings package initialization.
"""

from decouple import config
from dotenv import load_dotenv

# Ensure development settings are not used in testing and production:
if not config('CI', default=False) and not config('HEROKU', default=False):
    # load and set environment variables from '.env.yml' or '.env.py' files
    # with django_envie

    load_dotenv('.env')

    from core.settings.development import *

if config('HEROKU', default=False):
    from core.settings.production import *

if config('TRAVIS_BUILD', default=False):
    from core.settings.test import *
