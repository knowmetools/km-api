###########
Development
###########

The API is built with Python using Django and Django Rest Framework.

***********************************
Recommended Development Environment
***********************************

If you are comfortable with setting up a python development environment and cloning the project, feel free to skip to the `development environment overview <dev-overview_>`_.


Prerequisites
=============

We use git_ for version control and generally follow the development model laid out `here <git-branching-model_>`_. If you are looking for a tool to assist in following this model, we recommend git-flow_, a tool made by the same people that created the development model.

This project runs on Python 3.4. You must have Python 3.4 installed to contribute. If you do not have it installed, you can find it `here <python34_>`_. To manage third-party Python packages, we use pipenv_.


.. _project-setup:

Project Setup
=============

The first step is to clone the environment::

    $ git clone git@github.com:knowmetools/km-api
    # Or, if you don't have SSH access
    $ git clone https://github.com/knowmetools/km-api

    # The remaining commands require you to be in the project directory
    $ cd km-api/

If you installed the ``git-flow`` extension, you can now setup the repository to use it::

    $ git flow init -d

We also recommend the following configuration options::

    $ git config gitflow.feature.finish.keepremote true
    $ git config gitflow.bugfix.finish.keepremote true

Finally, install the project requirements ::

    $ pipenv install --dev

The final step is to create a ``.env`` file in the root of your project. This file will be read by any commands executed through ``pipenv``. For convenience, create the file with the contents::

    DJANGO_DEBUG=true

Linting
=======

We use flake8_ to lint our code, which is a tool for checking compliance with python's style guide: pep8_. To lint the source code, run flake8 from the project root::

    $ pipenv run flake8

If you want to run the linter on every commit, which is useful because our CI tool fails a build with linting errors, you can install flake8's git hook::

    $ pipenv run flake8 --install-hook git
    $ git config flake8.lazy true
    $ git config flake8.strict true

The configuration options ensure that only the code being committed is linted, and that linting errors will stop the commit process.


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

    $ pipenv run km_api/manage.py runserver


Running Tests
=============

Tests are run with pytest_. To run the tests, make sure the requirements are installed and run the tests::

    $ pipenv install --dev
    $ pipenv run pytest km_api/


Building Docs
=============

We use sphinx for building documentation, and the docs are automatically published using ReadTheDocs. If you want to build the docs locally, install the requirements and run the build command::

    $ pipenv install -r requirements/docs.txt
    $ cd docs
    $ pipenv run make html


.. _flake8: http://flake8.pycqa.org/en/latest/
.. _git: https://git-scm.com/downloads
.. _git-branching-model: http://nvie.com/posts/a-successful-git-branching-model/
.. _git-flow: https://github.com/nvie/gitflow
.. _pep8: https://www.python.org/dev/peps/pep-0008/
.. _pipenv: https://pipenv.readthedocs.io/en/latest/
.. _pytest: https://docs.pytest.org/en/latest/
.. _python34: https://www.python.org/downloads/release/python-343/
