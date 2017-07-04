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


# SSL Settings

CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True


# Static files configuration

DEFAULT_FILE_STORAGE = 'custom_storages.backends.MediaStorage'
STATICFILES_STORAGE = 'custom_storages.backends.StaticStorage'


# S3 Configuration

AWS_AUTO_CREATE_BUCKET = True
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=31536000',
}
AWS_S3_REGION_NAME = 'us-east-1'
AWS_STORAGE_BUCKET_NAME = os.environ['STATIC_BUCKET']
