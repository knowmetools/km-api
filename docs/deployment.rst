##########
Deployment
##########

We use Ansible_ and Terraform_ to deploy our application. Terraform is responsible for provisioning our infrastructure, and Ansible is used to configure our servers.

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

DJANGO_APPLE_RECEIPT_VALIDATION_ENDPOINT
----------------------------------------

**Default:** ``https://sandbox.itunes.apple.com/verifyReceipt``

The endpoint used to verify subscription receipts from Apple. This can take one of two values:

* ``https://sandbox.itunes.apple.com/verifyReceipt``
* ``https://buy.itunes.apple.com/verifyReceipt``

DJANGO_AWS_APPLICATION_NAME
---------------------------

**Default:** ``Know Me API``

The name of the application in AWS. This is used to group logs for CloudWatch.

DJANGO_AWS_REGION
-----------------

**Default:** ``us-east-1``

The AWS region to use for services such as S3 and SES.

DJANGO_CLOUDWATCH_LOGGING
-------------------------

**Default:** ``False``

Set to ``True`` (case insensitive) to enable logging to AWS CloudWatch.

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

DJANGO_HTTPS
------------

**Default:** ``False``

Set to ``True`` (case insensitive) if the application is served over HTTPS.

DJANGO_IN_MEMORY_FILES
----------------------

**Default:** ``False``

Set to ``True`` (case insensitive) to store static files in memory. This is mainly used for testing.

DJANGO_MAILCHIMP_API_KEY
------------------------

**Default:** ``''``

An API key for Mailchimp that is used to sync user emails to a mailing list. Only takes effect when ``DJANGO_MAILCHIMP_ENABLED`` is ``True``.

DJANGO_MAILCHIMP_ENABLED
------------------------

**Default:** ``False``

Set to ``True`` (case insensitive) to enable syncing of user emails with a Mailchimp list. Requires the following settings to be provided:

* ``DJANGO_MAILCHIMP_API_KEY``
* ``DJANGO_MAILCHIMP_LIST_ID``

DJANGO_MAILCHIMIP_LIST_ID
-------------------------

**Default:** ``''``

The ID of the Mailchimp list to sync user emails to. Only takes effect when ``DJANGO_MAILCHIMP_ENABLED`` is ``True``.

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


**************
Infrastructure
**************

We use Terraform to easily provision the infrastructure for multiple environments through the use of workspaces. Each workspace corresponds to a completely separate set of resources.

.. note::

    The ``default`` workspace, which is what Terraform uses if you don't explicitly select a workspace, corresponds to the ``dev`` workspace.

Each environment ends up being available at ``<env>.toolbox.knowmetools.com``.


Modifying the Infrastructure
============================

Prerequisites
-------------

  * AWS credentials with the appropriate permissions
  * Terraform must be `installed <terraform-install_>`_


File Organization
-----------------

All Terraform code is stored in the :file:`deploy/terraform` directory. The :file:`main.tf` file contains the configuration for deploying all the infrastructure for the project. :file:`variables.tf` contains the variables used to configure the deployment and their defaults, and :file:`outputs.tf` describes what is output after applying the configuration.


Initialization
--------------

Before performing any ``terraform`` commands, we must initialize Terraform. This does some basic checks and installs any necessary plugins. From the directory containing the terraform configuration, run::

    $ terraform init


Applying Changes
----------------

Applying changes to the infrastructure is broken down into two parts. First we plan out the changes that will be made::

    $ terraform plan -out tfplan

After ensuring that the proposed changes are reasonable, those changes can be applied::

    $ terraform apply tfplan


*************
Configuration
*************

We use Ansible to apply software configurations to our servers.


Modifying the Configuration Process
===================================

Prerequisites
-------------

  * SSH access to the webservers. If you were the one to provision the infrastructure, this should be set up automatically.
  * Ansible must be `installed <ansible-install_>`_
  * Access to the password for the Ansible Vault. This is available in the team's 1password vault.


File Organization
-----------------

All Ansible configuration files are in the :file:`deploy/ansible` directory. The :file:`env_vars` directory contains environment specific configurations. Variables that only apply to the webservers are in the :file:`group_vars/webservers` directory.


Deployment Requirements
-----------------------

We make use of a few different third party Ansible roles. These roles are listed in :file:`requirements.yml` and need to be installed before running the playbook::

    $ ansible-galaxy install -r requirements.yml


Credentials
-----------

Sensitive information used in configuring our servers is stored using Ansible's Vault system. When deploying, you must be able to decrypt this vault. The easiest way to do this is store the Vault password in a file and pass that file in when running the playbook::

    $ echo "<vault password>" > VAULT_PASSWORD_FILE

.. warning::

    The file name :file:`VAULT_PASSWORD_FILE` is excluded from version control by our :file:`.gitignore` configuration. If you name this file anything else, make sure it is not added to git.

The password can then be passed to Ansible as follows::

    $ ansible-playbook --vault-password-file VAULT_PASSWORD_FILE my-playbook.yml


Inventory
---------

Ansible has the concept of an inventory file which describes the servers we are targeting. A new inventory file should be created for each environment being configured. You can use the :file:`dev` inventory file as a template.

The inventory file then needs to be passed to Ansible::

    $ ansible-playbook -i my-inventory-file my-playbook.yml


Extra Variables
---------------

Sometimes it is useful to be able to configure Ansible variables from the command line when running the playbook. This is particularly useful when you need to pass in information output from Terraform after provisioning the application's infrastructure.

These variables are passed to Ansible at runtime with the ``-e`` flag::

    $ ansible-playbook -e foo='bar' my-playbook.yml

Including Terraform Outputs
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In general, Terraform outputs can be retrieved (from the Ansible directory) with the following command::

    $ cd ../terraform && terraform output <name>

If used in a subshell, this can be used to dynamically include Terraform outputs when running Ansible commands.


Example Run
-----------

Putting together all the configurations described above, an example run might look like::

    $ ansible-playbook \
        -i dev \
        --vault-password-file VAULT_PASSWORD_FILE \
        -e db_endpoint="$(cd ../terraform && terraform output database)" \
        -e static_bucket="$(cd ../terraform && terraform output static_bucket)" \
        deploy.yml

We also have a shell script to facilitate the above process. This shell script is located in the :file:`deploy` directory, and can be run as follows::

  $ deploy.sh ansible/ dev terraform/ default

The positional arguments are the relative path to the Ansible playbook directory, the name of the Ansible inventory file, the relative path to the Terraform configuration directory, and the name of the Terraform workspace to use, respectively.


.. _Ansible: http://docs.ansible.com/ansible/latest/index.html
.. _Terraform: https://www.terraform.io/
.. _ansible-install: http://docs.ansible.com/ansible/latest/intro_installation.html
.. _terraform-install: https://www.terraform.io/intro/getting-started/install.html
