"""Production settings.
"""

import datetime
import os

from km_api.settings import *       # noqa


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


# Production only apps

INSTALLED_APPS += [         # noqa
    # Third Party Apps
    'corsheaders',
    'raven.contrib.django.raven_compat',
    'storages',

    # Custom Apps
    'custom_storages',
]


# Production only middleware

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
] + MIDDLEWARE              # noqa


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


# Authentication Configuration

PASSWORD_RESET_LINK_TEMPLATE = os.environ.get(
    'PASSWORD_RESET_LINK_TEMPLATE',
    'https://example.com/change-password/?key={key}')


# Email Settings

AWS_SES_REGION_NAME = os.environ.get('AWS_REGION', 'us-east-1')
EMAIL_BACKEND = 'django_ses.SESBackend'
EMAIL_CONFIRMATION_EXPIRATION_DAYS = int(os.environ.get(
    'EMAIL_CONFIRMATION_EXPIRATION_DAYS',
    '1'))
EMAIL_CONFIRMATION_LINK_TEMPLATE = os.environ.get(
    'EMAIL_CONFIRMATION_LINK_TEMPLATE',
    'https://example.com/confirm-email?key={key}')


# SSL Settings

CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True


# Static files configuration

DEFAULT_FILE_STORAGE = 'custom_storages.backends.MediaStorage'
STATICFILES_STORAGE = 'custom_storages.backends.StaticStorage'


# CORS Configurations
# https://github.com/ottoyiu/django-cors-headers#configuration

CORS_ORIGIN_ALLOW_ALL = True


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
    os.path.join(BASE_DIR, 'layer.pem'))        # noqa


# MailChimp Configuration

MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY', '')
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
        'level': 'INFO',
        'handlers': ['file', 'sentry'],
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
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',        # noqa
            'formatter': 'standard',
        },
    },
    'loggers': {
        'boto3.resources.action': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.request': {
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}
