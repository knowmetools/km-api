"""Custom storage backends.
"""

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    Storage class for media files.

    Prefixes all file paths with ``media/``.
    """

    default_acl = "private"
    encryption = True
    location = "media"


class StaticStorage(S3Boto3Storage):
    """
    Storage class for static files.

    Prefixes all file paths with ``static/``.
    """

    default_acl = "public-read"
    location = "static"
    querystring_auth = False
