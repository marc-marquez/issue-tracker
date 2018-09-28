from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CLEARDB_DATABASE_URL = os.environ.get('CLEARDB_DATABASE_URL')

parsed_url = dj_database_url.parse(CLEARDB_DATABASE_URL)

# Load the ClearDB connection details from the environment variable
DATABASES = {
    'default': parsed_url
}

# Stripe environment variables
STRIPE_PUBLISHABLE = os.environ.get('STRIPE_PUBLISHABLE')
STRIPE_SECRET = os.environ.get('STRIPE_SECRET')

SITE_URL = 'https://mm-issue-tracker.herokuapp.com/'
ALLOWED_HOSTS.append('mm-issue-tracker.herokuapp.com')