#########
Changelog
#########

**************
In Development
**************

Features
  * :issue:`379`: Add endpoint to retrieve/update a user's Know Me subscription through Apple.

Miscellaneous
  * Completely changed the way that settings are provided. Rather than being specified in a separate python file that is then imported, behavior is now set through environment variables.
  * :issue:`383`: Removed MailChimp integration.


******
v1.4.1
******

Bug Fixes
  * :issue:`371`: Restore journal owner's ability to delete user comments.


******
v1.4.0
******

Features
  * :issue:`349`: Customize email templates for account related actions.
  * :issue:`364`: Add admin view for listing users.

Bug Fixes
  * :issue:`368`: Fix incorrect app store link in invitation notification email.


******
v1.3.0
******

Features
  * :issue:`236`: Add email notifications when a user is invited to view another user's profiles.


******
v1.2.2
******

Fix issue where users could upgrade their own accounts to have staff permissions.


******
v1.2.1
******

Bug Fixes
  * :issue:`357`: Add user account image to Know Me user list response data.
  * :issue:`358`: Fix users not being able to delete accessors granting them access to another user's informtion.


******
v1.2.0
******

Features
  * :issue:`354`: Add Know Me user information to accessor response.

Bug Fixes
  * :issue:`352`: Remove duplicate entry from user list.

Miscellaneous
  * :issue:`355`: Bump package versions


******
v1.1.0
******

Features
  :issue:`346`: Add endpoint to list previously accepted accessors.
  :issue:`347`: Allow users granted access by an accessor to delete that accessor.


******
v1.0.2
******

Bug Fixes
  :issue:`341`: Fix issue with list entries not being orderable.
  :issue:`343`: Fix bug with duplicate rows when selecting Know Me users.
  :issue:`345`: Fix issue with sharing errors not being caught and rendered.


******
v1.0.1
******

:issue:`337`: Fix issue with API documentation crashing.


******
v1.0.0
******

Breaking Changes
  * :issue:`296`: Add separate endpoint to accept an accessor.
  * :issue:`316`: Paginate journal entries. The entries are now nested under the ``results`` key, and there is additional information returned such as the total number of entries and the URLs for the next and previous pages. Entries are listed in reverse chronological order.
  * :issue:`332`: Remove ability to manually create a Know Me user. As per :issue:`263`, a Know Me user is automatically created for each registered user.

Features
  * :issue:`233`: Add config endpoint for Know Me app. It contains information such as the lowest useable iOS app version.
  * :issue:`259`: Add optional profile image for users.
  * :issue:`263,277`: Automatically create a Know Me user for each user. The Know Me user's image defaults to the user's profile image.
  * :issue:`278`: Include information about the user granted access through an accessor.
  * :issue:`299`: Add additional information to media resources. The resources can have a link instead of a file, and they have an integer to hint how they should be styled.
  * :issue:`306`: Add tracking of legacy users. The list of legacy users can be viewed/updated by staff.
  * :issue:`313`: Expose if a user is a staff member through the profile endpoint.
  * :issue:`321`: Allow media resources to be detached from profile items.
  * :issue:`326`: The Know Me user owned by the requesting user is guaranteed to be the first element in the list returned from ``/know-me/users/``. Each user in the list also has a new ``is_owned_by_current_user`` boolean attribute.
  * :issue:`328`: Increase maximum upload size to 100MB.


******
v0.9.3
******

Bug Fixes
  * :issue:`324`: Fix handling of duplicate accessors.
  * :issue:`325`: Fix crash when listing Know Me user accessors as an unauthenticated user.
  * :issue:`327`: Return journal entry permissions at the list level, rather than only from the detail endpoint.
  * :issue:`329`: Add missing attribute indicating if a profile is private or not.


******
v0.9.2
******

:issue:`317`: Fix error when attaching a media resource to a profile item.


******
v0.9.1
******

:issue:`276`: Add missing journal entries URL to Know Me user information.


******
v0.9.0
******

Features
  * :issue:`191,193,303`: Allow profiles and their components to be manually ordered.
  * :issue:`235`: Add timestamps to remaining models.
  * :issue:`300`: Send the correct URLs in account emails.

Bug Fixes
  * :issue:`271`: Fix deployment failing with newly provisioned servers.
  * :issue:`295`: Fix MailChimp integration.


******
v0.8.0
******

Breaking Changes
  * :issue:`253,282`: Massive rewrite of profile features. This is a backwards incompatible change that modifies endpoints and the data returned from profile endpoints in addition to requiring a complete database wipe.
  * :issue:`258`: Require multiple calls to return full profile.
  * :issue:`267`: Refactor accessor permission fields. The permissions are now encompassed in a single ``is_admin`` field.

Features
  * :issue:`246,247,251`: Add endpoints for managing journal entries.
  * :issue:`248,249,252`: Add endpoints for managing comments on journal entries.
  * :issue:`250`: Add searching for journal entries.
  * :issue:`267`: All models related to the Know Me app have creation and last-updated timestamps.
  * :issue:`276`: Return URLs in Know Me user list rather than only from the detail endpoint.

Bug Fixes
  * :issue:`254`: Fix Ansible creating duplicate crontab entries.
  * :issue:`261`: Fix permissions on ``KMUser`` instances not respecting sharing.
  * :issue:`262`: Fix access to private profiles being too open.
  * :issue:`265`: Fix inability to tear down Terraform-provisioned infrastructure.

Miscellaneous
  * :issue:`211`: Remove old "emergency" models.
  * :issue:`273`: Document release process.


******
v0.7.1
******

Bug Fixes
  * :issue:`244`: Fix issue with registration serializer.


******
v0.7.0
******

Developed "Bookshelf" as a rework of the old "Gallery".

Breaking Changes
  * Switched to third party account management package. This modified the endpoints used for email management, password resets, and registration. Also, the transition removed a lot of our account related models and modified their migrations. This means the existing database must be wiped and recreated.
  * :issue:`209`: Removed "emergency" related content.
  * :issue:`214`: Removed ``is_default`` field from profiles.
  * :issue:`239`: Removed Layer integration. This means Layer authentication tokens can no longer be obtained from the API.

Features
  * :issue:`212,217`: Added categories for media resources.
  * :issue:`213`: Add endpoint for listing media resources.

Bug Fixes
  * :issue:`224`: Fix issue with incorrect filtering of list views.

Miscellaneous
  * :issue:`208`: Switched to autogenerated documentation.


******
v0.6.1
******

Bug Fixes:
  * :issue:`225`: Fix production deployments being deployed to the staging environment.


******
v0.6.0
******

Implement sharing of profiles.

Features:
  * :issue:`154`: Allow profiles to be marked as private. Private profiles are not accessible by shared users unless they are explicitly granted access.

Bug Fixes:
  * :issue:`142`: Add missing migrations.
  * :issue:`139,197`: Add ability to share profiles with other users.
  * :issue:`177`: Fix issue with trying to register with an email address that is already being used.


******
v0.5.3
******

Update dependency versions.


******
v0.5.2
******

Bug Fixes
  * :issue:`195`: Fix issue with some endpoints only accepting a single-digit ID.


******
v0.5.1
******

Bug Fixes
  * :issue:`143`: Fix missing field on emergency contact admin page.


******
v0.5.0
******

This release was focused on renaming the components of a Know Me user's profile. As a result of this renaming, this release will break all existing data related to Know Me. This change also caused several endpoints to be renamed. The most relevant issue here is :issue:`65`.

* ``/know-me/gallery-items/*`` to ``/know-me/media-resources/*``
* ``/know-me/profiles/*`` to ``/know-me/users/*``
* ``/know-me/rows/*`` to ``/know-me/topics/*``

Breaking Changes
  * :issue:`66`: Remove grouped and paged row types.
  * :issue:`85`: Separated content for different types of profile items into different models. This means the data (other than name) from existing profile items is lost.

Features
  * :issue:`67`: Add emergency contacts for Know Me users.
  * :issue:`68,100,112`: Add list-type profile items.
  * :issue:`79,91,96`: Add ability for users to manage their emergency items.

Bug Fixes
  * :issue:`70`: Fixed regression in the error returned when attempting to log in with an unverified email address.
  * :issue:`75`: Fix parsing of JSON requests.

******
v0.4.0
******

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


******
v0.3.0
******

Features
  * :issue:`29,30,31`: Automatically sync user info to a MailChimp list.

Miscellaneous
  * :issue:`32`: Ignore reports about disallowed hosts.


******
v0.2.0
******

Breaking Changes
  * :issue:`18`: Flattened URL structure.
  * :issue:`21`: Moved Layer authentication to the ``/auth/layer/`` endpoint.

Features
  * :issue:`12`: Add logging in production.
  * :issue:`14`: Refactor permissions implementation using ``dry-rest-permissions`` package.
  * :issue:`19,20`: Add documentation.

Bug Fixes
  * :issue:`9`: Ensure passwords are validated.
