from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

import dj_database_url

# Load the ClearDB connection details from the environment variable
#CLEARDB_DATABASE_URL = os.environ.get('CLEARDB_DATABASE_URL')
#print("DATABASE: " + str(CLEARDB_DATABASE_URL))

db_config = dj_database_url.config()
if db_config:
    DATABASES['default'] = db_config
    #DATABASES = {
    #    'default': dj_database_url.config(CLEARDB_DATABASE_URL)
    #}

# Stripe environment variables
STRIPE_PUBLISHABLE = os.environ.get('STRIPE_PUBLISHABLE')
STRIPE_SECRET = os.environ.get('STRIPE_SECRET')