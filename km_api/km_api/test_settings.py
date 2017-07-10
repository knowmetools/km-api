"""Settings for running tests.
"""

from km_api.settings import *       # noqa


SECRET_KEY = 'secret'


# Store media files in memory rather than on disk

DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'


# Disable Mailchimp integration while testing

MAILCHIMP_API_KEY = 'fake-api-key'
MAILCHIMP_ENABLED = False
MAILCHIMP_LIST_ID = 'list'
