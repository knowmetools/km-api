#############
Release Cycle
#############

Our release cycle and development process is based on `A Successful Git Branching Model <git-branching-model_>`_. To assist in the use of this model, we recommend the use of git-flow_, which is a tool built on top of Git.

This document describes how we integrate the described branching model with GitHub, and the specifics of releasing new versions.

.. note::

    We assume that ``git-flow`` has been installed and configured as described in :ref:`project-setup`.


******************
Normal Development
******************

Most development should occur in the form of work on ``feature/*`` or ``bugfix/*`` branches. These branches are created from and merged back into the ``develop`` branch.

With regards to GitHub, no work should be done without the presence of an issue outlining the required work. This process makes it easy to ensure that branches (and the resulting pull requests) only address one thing at a time, resulting in easier code reviews.


Features
========

Features are the addition of new features or attributes that didn't exist before. To start a new feature::

    $ git flow feature start my-feature-name

The created feature branch should be pushed to GitHub, and a pull request should be opened. This allows us to perform a code review and ensure that all automated tests pass. We encourage pull requests for feature branches to be opened early in the development process so that feedback can be provided sooner rather than later.

Once the feature is complete, tests have passed, and the code has been reviewed, someone with write permissions on the ``develop`` branch can run the following::

    $ git flow feature finish my-feature-name

The completion of a feature is greatly assisted if the feature is first squashed down to one commit. This can be accomplished by the following::

    $ git checkout develop
    $ git pull
    $ git checkout feature/my-feature-name
    $ git rebase -i develop

When rebasing, simply squash down all the commits, and ensure that the final commit message describes the cummulative change.


Bug Fixes
=========

Bug fixes should be used to correct unexpected or broken behavior that is not critical to the production environment. To start a new bugfix::

    $ git flow bugfix start my-bugfix

The rest of the process is the same as the one for features.


************
New Releases
************

Releases are created based on the development branch. After creating a release branch, no new features should be added on to that release (but they can continue to be added to the ``develop`` branch). To start a new release::

    $ git flow release start vX.Y.0

These releases should always have a 0 as the patch number. The creation of a release branch should be **IMMEDIATELY** followed by the bumping of the minor or major version using bumpversion_::

    $ bumpversion [minor|major]

Any additional tweaks or bug fixes required for the features that are a part of this release can continue to be added on to this release branch. The release can then be completed with::

    $ git flow release finish vX.Y.0

During this command, you will be prompted for a message for the tag being created. This message should be ``Release vX.Y.0``. After the command completes, make sure all impacted Git artifacts are pushed::

    $ git push --tags && git push origin master && git push


********
Hotfixes
********

Hotfixes are used when there is a critical issue in production, and a fix cannot be delayed until the next release.

.. warning::

    Hotfixes should be used with caution because they typically do not go through the same pull request and review process that other changes do.

To start a new hotfix, first inspect the current version number. The hotfix branch should be created with the current version's patch number incremented by one. For example, if the current version is ``v1.4.0``, the command would be::

    $ git flow hotfix start v1.4.1

The creation of a hotfix branch should be **IMMEDIATELY** followed by the bumping of the patch number using bumpversion_::

    $ bumpversion patch

Once all relevant changes have been made and carefully tested, the hotfix can be completed and merged back::

    $ git flow hotfix finish vX.Y.Z

The message for the newly created tag should be ``Release vX.Y.Z``. After the process completes, make sure all Git artifacts are pushed::

    $ git push --tags && git push origin master && git push


.. _bumpversion: https://github.com/peritus/bumpversion
.. _git-branching-model: http://nvie.com/posts/a-successful-git-branching-model/
