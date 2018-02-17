"""Production settings.
"""

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


# Email Settings

AWS_SES_REGION_NAME = 'us-east-1'
EMAIL_BACKEND = 'django_ses.SESBackend'


# SSL Settings

CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True


# Static files configuration

DEFAULT_FILE_STORAGE = 'custom_storages.backends.MediaStorage'
STATICFILES_STORAGE = 'custom_storages.backends.StaticStorage'


# CORS Configurations
# https://github.com/ottoyiu/django-cors-headers#configuration

CORS_ORIGIN_ALLOW_ALL = True


# S3 Configuration

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=31536000',
}
AWS_S3_REGION_NAME = 'us-east-1'


# Attempt to use settings uploaded by Ansible

try:
    from km_api.local_settings import *     # noqa
except ImportError:
    pass
