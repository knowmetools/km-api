"""Production settings.
"""

import datetime

from km_api.settings import *       # noqa

DEBUG = False


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


# Authentication Configuration

PASSWORD_RESET_EXPIRATION_HOURS = 1
PASSWORD_RESET_LINK_TEMPLATE = 'https://example.com/change-password/?key={key}'


# Email Settings

AWS_SES_REGION_NAME = 'us-east-1'
EMAIL_BACKEND = 'django_ses.SESBackend'
EMAIL_CONFIRMATION_EXPIRATION_DAYS = 1
EMAIL_CONFIRMATION_LINK_TEMPLATE = 'https://example.com/confirm-email?key={key}'    # noqa


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


# Layer Configuration

LAYER_IDENTITY_EXPIRATION = datetime.timedelta(seconds=300)


# Attempt to use settings uploaded by Ansible

try:
    from km_api.local_settings import *     # noqa
except ImportError:
    pass
