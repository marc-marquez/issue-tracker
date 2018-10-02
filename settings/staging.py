from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

JAWSDB_DATABASE_URL = os.environ.get('JAWSDB_URL')

# Load the ClearDB connection details from the environment variable
DATABASES = {
    'default': dj_database_url.config(JAWSDB_DATABASE_URL)
}

# Stripe environment variables
STRIPE_PUBLISHABLE = os.environ.get('STRIPE_PUBLISHABLE')
STRIPE_SECRET = os.environ.get('STRIPE_SECRET')

SITE_URL = 'https://mm-issue-tracker.herokuapp.com/'
ALLOWED_HOSTS.append('mm-issue-tracker.herokuapp.com')