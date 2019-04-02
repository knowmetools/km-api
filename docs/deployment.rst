##########
Deployment
##########

For an example of how to deploy the application, see `knowmetools/km-api-deployment`_.

*********************
Environment Variables
*********************

The following environment variables can be used to modify the application's behavior.

.. note::

    The application will only attempt to use a Postgres database if all of ``DJANGO_DB_HOST``, ``DJANGO_DB_NAME``, ``DJANGO_DB_PASSWORD``, ``DJANGO_DB_PORT``, and ``DJANGO_DB_USER`` are set. If any of these settings are not provided, we fall back to a local SQLite database.

DJANGO_ALLOWED_HOSTS
--------------------

**Default:** ``''``

A comma separated list of allowed hosts.

.. note::

    This must be set if ``DJANGO_DEBUG`` is set to ``False``.

DJANGO_APPLE_PRODUCT_CODES_KNOW_ME_PREMIUM
------------------------------------------

**Default:** ``''``

A comma separated list of product IDs that should be accepted to mark purchases of Know Me's premium version. This allows us to have multiple in-app purchases that activate the premium version. For example, we can have one subscription be monthly and another be billed annually.

DJANGO_APPLE_RECEIPT_VALIDATION_ENDPOINT
----------------------------------------

**Default:** ``https://sandbox.itunes.apple.com/verifyReceipt``

The endpoint used to verify subscription receipts from Apple. This can take one of two values:

* ``https://sandbox.itunes.apple.com/verifyReceipt``
* ``https://buy.itunes.apple.com/verifyReceipt``

DJANGO_APPLE_SHARED_SECRET
--------------------------

**Default:** ``''``

The shared secret used to verify receipts with the Apple store.

.. note::

    This must be provided. If it is not, all Apple receipt validations will fail.

DJANGO_AWS_REGION
-----------------

**Default:** ``us-east-1``

The AWS region to use for services such as S3 and SES.

DJANGO_DB_HOST
--------------

**Default:** ``localhost``

The hostname of the Postgres database to connect to.

DJANGO_DB_NAME
--------------

**Default:** ``''``

The name of the Postgres database to connect to.

DJANGO_DB_PASSWORD
------------------

**Default:**: ``''``

The password of the user that the application connects to the Postgres database as.

DJANGO_DB_PORT
--------------

**Default:** ``5432``

The port to connect to the Postgres database on.

DJANGO_DB_USER
--------------

**Default:** ``''``

The name of the user to connect to the Postgres database as.

DJANGO_DEBUG
------------

**Default:** ``False``

Set to ``True`` (case insensitive) to enable Django's debug mode.

DJANGO_EMAIL_VERIFICATION_URL
-----------------------------

**Default:** ``https://example.com/verify/{key}'``

The template used to construct links for verifying a user's email address. The ``{key}`` portion of the template will be replaced with a unique token.

.. _DJANGO_HTTPS:

DJANGO_HTTPS
------------

**Default:** ``False``

Set to ``True`` (case insensitive) if the application is served over HTTPS.

DJANGO_HTTPS_LOAD_BALANCER
--------------------------

**Default:** ``False``

Set to ``True`` (case insensitive) if the application is served over HTTPS but is located behind a load balancer that terminates SSL. If this is enabled, requests with the header ``HTTP_X_FORWARDED_PROTO`` set to ``https`` will be treated as if they came in over HTTPS.

.. note::

    This has no effect unless :ref:`DJANGO_HTTPS` is set to ``True``.

DJANGO_IN_MEMORY_FILES
----------------------

**Default:** ``False``

Set to ``True`` (case insensitive) to store static files in memory. This is mainly used for testing.

DJANGO_MEDIA_ROOT
-----------------

**Default:** ``''``

The location on the server's filesystem to store user uploaded files at. This setting has no effect when ``DJANGO_S3_STORAGE`` is ``True``.

DJANGO_PASSWORD_RESET_URL
-------------------------

**Default:** ``https://example.com/reset/{key}``

The template used to construct password reset links. The ``{key}`` portion of the template will be replaced with a unique token.

DJANGO_S3_AWS_REGION
--------------------

**Default:** ``$DJANGO_AWS_REGION``

The AWS region that the S3 bucket used to store files is located in. Only takes effect when ``DJANGO_S3_STORAGE`` is ``True``.

DJANGO_S3_BUCKET
----------------

**Default:** ``''``

The name of the S3 bucket to store files in. Only takes effect when ``DJANGO_S3_STORAGE`` is ``True``.

DJANGO_S3_STORAGE
-----------------

**Default:** ``False``

Set to ``True`` (case insensitive) to enable storage of static and user uploaded files in an S3 bucket. Requires the following settings to be provided:

* ``DJANGO_S3_BUCKET``

DJANGO_SECRET_KEY
-----------------

**Default:** ``secret``

.. warning::

    The default value is only used if ``DJANGO_DEBUG`` is set to ``True``. This is to avoid exposing a known secret key in a production environment.

The secret key that Django uses for a few security operations.

DJANGO_SENTRY_DSN
-----------------

**Default:** ``''``

The *Data Source Name* for the application's Sentry project. If provided logging of warnings and errors to Sentry is enabled.

DJANGO_SENTRY_ENVIRONMENT
-------------------------

**Default:** ``default``

The name of the environment that should be provided as context when logging to Sentry. Only takes effect when ``DJANGO_SENTRY_DSN`` is provided.

DJANGO_SES_AWS_REGION
---------------------

**Default:** ``$DJANGO_AWS_REGION``

The AWS region to send SES emails from. Only takes effect when ``DJANGO_SES_ENABLED`` is ``True``.

DJANGO_SES_ENABLED
------------------

**Default:** ``False``

Set to ``True`` (case insensitive) to enable sending of emails using AWS SES.

DJANGO_STATIC_ROOT
------------------

**Default:** ``''``

The location on the server's filesystem to store static files at. This setting has no effect when ``DJANGO_S3_STORAGE`` is ``True``.


.. _knowmetools/km-api-deployment: https://github.com/knowmetools/km-api-deployment
