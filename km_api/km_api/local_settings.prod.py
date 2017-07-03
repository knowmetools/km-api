"""Production settings.
"""

import os


# Set the secret key from an environment variable. We use the bracket
# notation so that a ``KeyError`` will be raised if we forget to set the
# variable.

SECRET_KEY = os.environ['SECRET_KEY']


# Set the hosts allowed to access the application

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')


# Enable debugging only if the appropriate environment variable is set.

DEBUG = os.environ.get('DEBUG', '').lower() == 'true'


# Use an external Postgres database.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}
