"""Settings for running tests.
"""

from km_api.settings import *       # noqa


SECRET_KEY = 'secret'


# Store media files in memory rather than on disk

DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
