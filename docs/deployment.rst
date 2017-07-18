==========
Deployment
==========

Deployment is handled through AWS' Elastic Beanstalk service. Tagged releases and commits on the ``develop`` branch are automatically deployed to production and staging, respectively.


---------------------
Environment Variables
---------------------

The application uses the following environment variables. These can be set from the Elastic Beanstalk interface.

ALLOWED_HOSTS (=[ ])
  A comma separated list of URLs that the app is accessible from.

AWS_REGION (=us-east-1)
  The region the project's AWS resources are running in.

DEBUG (=False)
  Set to ``True`` (case insensitive) to enable Django's debug mode.

EMAIL_CONFIRMATION_EXPIRATION_DAYS (=1)
  An integer specifying the number of days an email confirmation is valid for.

EMAIL_CONFIRMATION_LINK_TEMPLATE (=https://example.com/confirm-email?key={key})
  A template for the URL a user should visit to validate their email. The value
  ``{key}`` in the template string will be replaced with the confirmation key.

LAYER_IDENTITY_EXPIRATION (=300)
  The expiration time of each Layer identity token in seconds. See Layer's `Identity Token documentation <layer-identity-token-docs_>`_ for more information.

LAYER_KEY_ID
  The ID of the key located at ``LAYER_RSA_KEY_FILE_PATH``. This can be found
  in Layer's organization dashboard. It should have the format ``layer:///keys/<key-content>``.

LAYER_PROVIDER_ID
  The provider ID of the Layer organization. This can be found in Layer's organization dashboard. It should have the format ``layer:///providers/<provider-id>``.

LAYER_RSA_KEY_FILE_PATH (=/etc/km-api/certs/layer-dev.pem)
  The path to the RSA key used to encode the identity tokens for Layer.

MAILCHIMP_API_KEY (='')
  The API key to use when using the MailChimp API.

MAILCHIMP_ENABLED (=False)
  Set to ``True`` (case insensitive) to enable syncing of user data to a MailChimp list. Requires ``MAILCHIMP_API_KEY`` and ``MAILCHIMP_LIST_ID`` to be set.

MAILCHIMP_LIST_ID (='')
  The ID of the MailChimp list to sync users to. Can be found under the list's "Settings" menu in "List name and campaign defaults".

PASSWORD_RESET_EXPIRATION_HOURS (=1)
  The number of hours a password reset's key is valid for.

PASSWORD_RESET_LINK_TEMPLATE (=https://example.com/change-password/?key={key})
  A template for the URL a user should visit to complete the password reset process. The value ``{key}`` in the template string will be replaced with the password reset key.

SECRET_KEY
  The secret key to use. This should be a long random string. See the `documentation <secret-key-docs_>`_ for details.

SENTRY_DSN
  The DSN to use for sentry logging. See the `documentation <sentry-dsn-docs_>`_ for details.

SENTRY_ENVIRONMENT (=staging)
  The environment to use when logging errors to sentry. This allows for differentiating between production and staging errors. For simplicity, this should be either ``staging`` or ``production``.

STATIC_BUCKET
  The name of the S3 bucket to store static and media files in. The IAM role that the webservers use must have access to this bucket. This bucket must be in the ``us-east-1`` region.


--------------------
Database Credentials
--------------------

If an RDS database is attached to the Elastic Beanstalk environment then these values will be set automatically. To use a different database, set the following environment variables. *This must be a PostgreSQL database.*

RDS_DB_NAME
  The database's name.

RDS_HOSTNAME:
  The hostname of the database.

RDS_PASSWORD:
  The password to connect to the database with.

RDS_PORT:
  The port to connect to the database on. This is usually 5432.

RDS_USERNAME:
  The username to connect to the database with.


.. _layer-identity-token-docs: https://docs.layer.com/sdk/web/authentication#identity-token
.. _secret-key-docs: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
.. _sentry-dsn-docs: https://docs.sentry.io/quickstart/#configure-the-dsn
