##########
Deployment
##########

We use Ansible_ and Terraform_ to deploy our application. Terraform is responsible for provisioning our infrastructure, and Ansible is used to configure our servers.


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
