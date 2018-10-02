from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': dj_database_url.config('LOCALHOST_DATABASE_URL')
}

ALLOWED_HOSTS.append('localhost')

# Stripe environment variables
STRIPE_PUBLISHABLE = os.environ.get('STRIPE_PUBLISHABLE')
STRIPE_SECRET = os.environ.get('STRIPE_SECRET')