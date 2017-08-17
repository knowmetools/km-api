==========
Deployment
==========

Deployment is handled with Ansible_ and deployed continuously with `Travis CI <travis-ci_>`_. Tagged releases are deployed to production and the ``develop``, ``hotfix/*``, and ``release/*`` branches are deployed to the staging environment.


--------
Overview
--------

The deployment is split into 3 main parts. First we provision the required infrastructure, then we bake the application into a reusable image, and finally we set up the webservers to use that image.

The provisioning process first creates all the security groups that we will use and configures rules for them so they can talk to each other. Next we create an RDS instance and set up our database on it.

The next part of the process is creating an image to launch our webservers from. To do this, we spin up an EC2 instance and set it up to serve our application. We then create an AMI from this machine.

The last part of the process is creating an autoscaling group using the AMI we just created. The autoscaling group handles the termination of existing instances running old versions and spinning up an appropriate number of servers with the new version. This group is then placed behind a load balancer.


--------------------------
Customizing the Deployment
--------------------------

There are a few places containing settings controlling the deployment process .

Non-sensitive information that affects only the application's behaviour is stored in ``km_api/km_api/production_settings.py``.

The rest of the deployment configuration is expressed using Ansible variables.

Infrastructure configuration is stored in the ``deploy/env_vars/`` folder. ``base.yml`` holds variables that are shared accross environments, while ``dev.yml`` and ``prod.yml`` store information specific to each environment.

The webserver configuration is stored in ``deploy/group_vars/amibuilder/``. These variables only apply to the software on the webservers.


-----------------
Manual Deployment
-----------------

Prerequisites
-------------

In order to run a deployment, you must first install the requirements.

.. note::

    Ansible defaults to using the system-wide python installation. This means that the requirements must be installed for that python version, or you can point Ansible at a different python interpreter with the ``--ansible-python-interpreter /path/to/python`` flag.

The deployment requirements are listed in ``requirements/deploy.txt``::

    $ pip install requirements/deploy.txt

After installing the deployment requirements, you must also install the required Ansible roles::

    $ cd deploy
    $ ansible-galaxy install -r requirements.yml


Credentials
-----------

The deployment process requires a password to decrypt the vault used to store other credentials as well as AWS credentials with permissions for the resources we use.

The vault password can be found in our team password vault. Pass it to Ansible with::

    $ echo "myvaultpass" > VAULT_PASSWORD_FILE
    $ export ANSIBLE_VAULT_PASSWORD_FILE=VAULT_PASSWORD_FILE

AWS credentials can also be specified as environment variables::

    $ export AWS_ACCESS_KEY_ID=your-access-key
    $ export AWS_SECRET_ACCESS_KEY=your-secret-key

The AWS credentials must have the following permissions:

* EC2

  * Create and edit security groups
  * Start and stop EC2 instances
  * Create AMIs
  * Create and edit load balancers
  * Create launch configurations
  * Create and edit autoscaling groups

* RDS

  * Create and edit RDS instances

* Route 53

  * Create and edit domain entries

Running the Playbook
--------------------

Before deploying, make sure you are in the ``deploy/`` directory.

To deploy to staging::

    $ ansible-playbook deploy.yml

To deploy to production::

    $ ansible-playbook -e 'env=prod' deploy.yml


.. _Ansible: http://docs.ansible.com/ansible/latest/index.html
.. _travis-ci: https://travis-ci.org/knowmetools/km-api
