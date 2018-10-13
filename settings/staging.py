from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

JAWSDB_URL = os.environ.get('JAWSDB_URL')

# Load the ClearDB connection details from the environment variable
DATABASES = {
    'default': dj_database_url.config(default=JAWSDB_URL)
}

# Stripe environment variables
STRIPE_PUBLISHABLE = os.environ.get('STRIPE_PUBLISHABLE')
STRIPE_SECRET = os.environ.get('STRIPE_SECRET')

SITE_URL = 'https://quo-vadimus.herokuapp.com/'
ALLOWED_HOSTS.append('quo-vadimus.herokuapp.com')