Changelog
=========


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
