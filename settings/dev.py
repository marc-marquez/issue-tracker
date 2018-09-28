from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   }
}

#import dj_database_url

#DATABASES = {}
# Load the ClearDB connection details from the environment variable
#CLEARDB_DATABASE_URL = os.environ.get('CLEARDB_DATABASE_URL')

#parsed_url = dj_database_url.parse(CLEARDB_DATABASE_URL)
#print(parsed_url)


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'heroku_41fd08de6cc6915',
#        'USER': 'bad41e77edb428',
#        'PASSWORD': '8bb00b3b',
#        'HOST': 'us-cdbr-iron-east-01.cleardb.net',
#        'PORT': None,
#    }
#}

# Stripe environment variables
STRIPE_PUBLISHABLE = os.environ.get('STRIPE_PUBLISHABLE')
STRIPE_SECRET = os.environ.get('STRIPE_SECRET')