
"""
Settings package initialization.
"""

import os

# Ensure development settings are not used in testing and production:
if not os.getenv('CI') and not os.getenv('HEROKU'):
    # load and set environment variables from '.env.yml' or '.env.py' files
    # with django_envie
    from dotenv import load_dotenv
    load_dotenv('.env')

    from development import *

if os.getenv('HEROKU'):
    from production import *
