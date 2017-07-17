===========
Development
===========

The API is built with Python using Django and Django Rest Framework.

-----------------------------------
Recommended Development Environment
-----------------------------------

If you are comfortable with setting up a python development environment and cloning the project, feel free to skip to the `development environment overview <dev-overview_>`_.

Prerequisites
-------------

We use git_ for version control and generally follow the development model laid out `here <git-branching-model_>`_. If you are looking for a tool to assist in following this model, we recommend git-flow_, a tool made by the same people that created the development model.

Since this is a Python project, we recommend using a virtualenv_ to manage the environment for the project. If you want to simplify the management of these virtual environments, we recommend using virtualenvwrapper_.

This project runs on Python 3.4, since that's the Python version available on Elastic Beanstalk, our hosting platform. Ideally your development environment also has Python 3.4 installed. If not, you can find it `here <python34_>`_

Project Setup
-------------

.. note::

    The following commands assume the ``virtualenvwrapper`` package is installed.

Before cloning the environment, create a virtual environment for the project's dependencies::

    $ mkproject --python=python3.4 km-api
    $ workon km-api

You can now clone the project. Since the directory will have already been created, we initialize an empty git repository and then add the project as a remote::

    $ git init
    $ git remote add origin https://github.com/knowmetools/km-api
    $ git pull origin develop

If you installed the ``git-flow`` extension, you can now setup the repository to use it::

    $ git flow init -d

Finally, install the project requirements appropriate for what you need. The ``test`` requirements should cover what you need, but if you want to build the documentation locally, install the ``docs`` requirements. If all you want to do is run the project locally, the ``base`` requirements are all you need.::

    $ pip install -r requirements/[base|docs|test].txt

Linting
-------

We use flake8_ to lint our code, which is a tool for checking compliance with python's style guide: pep8_. To lint the source code, run flake8 from the project root::

    $ flake8

If you want to run the linter on every commit, which is useful because our CI tool fails a build with linting errors, you can install flake8's git hook::

    $ flake8 --install-hook git
    $ git config flake8.lazy true
    $ git config flake8.strict true

The configuration options ensure that only the code being committed is linted, and that linting errors will stop the commit process.

.. _dev-overview:

------------------------
Dev Environment Overview
------------------------

If you have not yet cloned the repository, do so and install the requirements::

    $ git clone https://github.com/knowmetools/km-api
    $ cd km-api
    $ pip install -r requirements/base.txt

Local Dev Server
----------------

Before running the dev server, you must create a file at ``km_api/km_api/local_settings.py``, relative to the project root, with the following content::

    # Extend from the base settings
    from km_api.settings import *       # noqa

    # A random string. This doesn't have to be anything complex for development
    SECRET_KEY = '<some secret key>'

    # Layer information can be found on Layer's dashboard.
    LAYER_KEY_ID = 'layer:///keys/<key content>'
    LAYER_PROVIDER_ID = 'layer:///providers/<provider id>'

You must also have the private key referenced by ``LAYER_KEY_ID`` located at ``km_api/layer.pem``. If you want to change the location of this file, set ``LAYER_RSA_KEY_FILE_PATH`` to point to that location.

Finally, run the dev server with::

    $ export DJANGO_SETTINGS_MODULE='km_api.local_settings'
    $ km_api/manage.py runserver

Running Tests
-------------

Tests are run with pytest_. To run the tests, make sure the requirements are installed and run the tests::

    $ pip install -r requirements/test.txt
    $ pytest

Building Docs
-------------

We use sphinx for building documentation, and the docs are automatically published using ReadTheDocs. If you want to build the docs locally, install the requirements and run the build command::

    $ pip install -r requirements/docs.txt
    $ cd docs
    $ make html


.. _flake8: http://flake8.pycqa.org/en/latest/
.. _git: https://git-scm.com/downloads
.. _git-branching-model: http://nvie.com/posts/a-successful-git-branching-model/
.. _git-flow: https://github.com/nvie/gitflow
.. _pep8: https://www.python.org/dev/peps/pep-0008/
.. _pytest: https://docs.pytest.org/en/latest/
.. _python34: https://www.python.org/downloads/release/python-343/
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/
