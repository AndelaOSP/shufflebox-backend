
"""
Settings package initialization.
"""

import os
from dotenv import load_dotenv

# Ensure development settings are not used in testing and production:
if not os.getenv('CI') and not os.getenv('HEROKU'):
    # load and set environment variables from '.env.yml' or '.env.py' files
    # with django_envie

    load_dotenv('.env')

    from shufflebox.settings.development import *

if os.getenv('HEROKU'):
    from shufflebox.settings.production import *

if os.getenv('TRAVIS_BUILD'):
    from shufflebox.settings.test import *
