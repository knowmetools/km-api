Changelog
=========

v0.5
----

Bug Fixes
  * :issue:`75`: Fix parsing of JSON requests.


v0.4
----

Breaking Changes
  * :issue:`27`: Move user profile view from ``/auth/profile/`` to ``/account/profile``.
  * :issue:`36,54`: Emails must be verified before being able to log in.
  * :issue:`42`: The user model was moved to the ``account`` app. This requires dropping any existing databases.

Features
  * :issue:`28`: Users can change their password.
  * :issue:`34`: Users can now request a password reset by email.
  * :issue:`47`: Allow users to manage their email addresses. They can now add/remove addresses and switch which one is the primary.
  * :issue:`50`: Users receive a notification when an email is added to their account.

Miscellaneous
  * :issue:`41`: Users can be authenticated by passing an ``email`` rather than a ``username`` to Django's ``authenticate`` function.
  * :issue:`46`: An admin user is created when the project is deployed.
  * :issue:`52`: Developers are no longer required to have a local settings file.


v0.3
----

Features
  * :issue:`29,30,31`: Automatically sync user info to a MailChimp list.

Miscellaneous
  * :issue:`32`: Ignore reports about disallowed hosts.


v0.2
----

Breaking Changes
  * :issue:`18`: Flattened URL structure.
  * :issue:`21`: Moved Layer authentication to the ``/auth/layer/`` endpoint.

Features
  * :issue:`12`: Add logging in production.
  * :issue:`14`: Refactor permissions implementation using ``dry-rest-permissions`` package.
  * :issue:`19,20`: Add documentation.

Bug Fixes
  * :issue:`9`: Ensure passwords are validated.
