"""Production settings.
"""

import datetime
import os


# Base directory for the project.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Set the secret key from an environment variable. We use the bracket
# notation so that a ``KeyError`` will be raised if we forget to set the
# variable.

SECRET_KEY = os.environ['SECRET_KEY']


# Set the hosts allowed to access the application

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS.extend([
    'localhost',
])


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


# Layer Configuration

LAYER_IDENTITY_EXPIRATION = datetime.timedelta(
    seconds=os.environ.get('LAYER_IDENTITY_EXPIRATION', 300))
LAYER_KEY_ID = os.environ['LAYER_KEY_ID']
LAYER_PROVIDER_ID = os.environ['LAYER_PROVIDER_ID']
LAYER_RSA_KEY_FILE_PATH = os.environ.get(
    'LAYER_RSA_KEY_FILE_PATH',
    os.path.join(BASE_DIR, 'layer.pem'))


# MailChimp Configuration

MAILCHIMP_ENABLED = os.environ.get('MAILCHIMP_ENABLED', '').lower() == 'true'
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID', '')


# Sentry Configuration (for logging)

RAVEN_CONFIG = {
    'dsn': os.environ['SENTRY_DSN'],
    'environment': os.environ.get('SENTRY_ENVIRONMENT', 'staging'),
}


# Logging Configuration

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',  # noqa
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/km-api/django-info.log',
            'formatter': 'standard',
            'backupCount': 5,
            'maxBytes': 5000000,    # 5 megabytes
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'sentry': {
            'level': 'INFO',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',        # noqa
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'sentry'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propogate': False,
        },
        'mailing_list': {
            'handlers': ['file', 'sentry'],
            'level': 'INFO',
            'propagate': True,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['file'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['file'],
            'propagate': False,
        },
    },
}
