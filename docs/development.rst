###########
Development
###########

The API is built with Python using Django and Django Rest Framework.

***********************************
Recommended Development Environment
***********************************

If you are comfortable with setting up a python development environment and
cloning the project, feel free to skip to the
`development environment overview <dev-overview_>`_.


Prerequisites
=============

We use git_ for version control and follow the general pattern of always having
a production-ready master branch with features developed on short-lived
branches.

This project runs on Python 3.6. You must have Python 3.6 installed to
contribute. If you do not have it installed, you can find it
`here <python36_>`_. To manage third-party Python packages, we use pipenv_.


.. _project-setup:

Project Setup
=============

The first step is to clone the environment::

    $ git clone git@github.com:knowmetools/km-api
    # Or, if you don't have SSH access
    $ git clone https://github.com/knowmetools/km-api

    # The remaining commands require you to be in the project directory
    $ cd km-api/

Next, install the project requirements ::

    $ pipenv install --dev

The final step is to create a ``.env`` file in the root of your project. This
file will be read by any commands executed through ``pipenv``. For convenience,
create the file with the contents::

    DJANGO_DEBUG=true
    DJANGO_MEDIA_ROOT=km_api/media

Linting
=======

We use a combination of flake8_ and black_ for linting and formatting our code,
respectively. To ensure that there are no formatting/linting errors on each
commit, we use the pre-commit_ tool. To install it, simply run::

    pipenv run pre-commit install

This will ensure that your code is formatted prior to every commit. If the tool
is somehow circumvented or not run, our CI process also runs the same checks and
will fail a build that has formatting or linting errors.


.. _dev-overview:

************************
Dev Environment Overview
************************

Quickstart
==========

Clone the project and install the dependencies::

    $ git clone git@github.com:knowmetools/km-api
    $ cd km-api
    $ pipenv install --dev


Local Dev Server
================

The development server can be run using the following command::

    $ pipenv run km_api/manage.py migrate
    $ pipenv run km_api/manage.py runserver


Running Tests
=============

Tests are run with pytest_. To run the tests, make sure the requirements are
installed and run the tests::

    $ pipenv install --dev
    $ pipenv run pytest km_api/


Building Docs
=============

We use sphinx for building documentation, and the docs are automatically
published using ReadTheDocs. If you want to build the docs locally, install the
requirements and run the build command::

    $ pipenv install -r requirements/docs.txt
    $ cd docs
    $ pipenv run make html


.. _black: https://github.com/ambv/black
.. _flake8: http://flake8.pycqa.org/en/latest/
.. _git: https://git-scm.com/downloads
.. _pipenv: https://pipenv.readthedocs.io/en/latest/
.. _pre-commit: https://pre-commit.com/
.. _pytest: https://docs.pytest.org/en/latest/
.. _python36: https://www.python.org/downloads/release/python-367/
