=======
Account
=======


-------
Profile
-------

A user's profile contains personal information about the user such as their email or name.

.. note::

    If you are looking to change a user's password, see the `Change Password <change-password_>`_ endpoint.

.. http:get:: /account/profile/

    Retrieve the requesting user's account information.

    :>json int id: The user's ID.
    :>json string email: The user's email address.
    :>json string first_name: The user's first name.
    :>json string last_name: The user's last name.

    :status 200: The user's information was successfully retrieved.

.. http:patch:: /account/profile/

    Update the requesting user's information.

    :<json string first_name: *(Optional)* The user's new first name.
    :<json string last_name: *(Optional)* The user's new last name.

    :>json int id: The user's ID.
    :>json string email: The user's email address.
    :>json string first_name: The user's first name.
    :>json string last_name: The user's last name.

    :status 200: The user's information was successfully updated.
    :status 400: Invalid request. Check the response data for details.


.. _change-password:

---------------
Change Password
---------------

.. http:post:: /account/change-password/

    Change the password of the currently authenticated user.

    :<json string old_password: The user's current password.
    :<json string new_password: The user's new password.

    :status 200: The user's password was successfully changed.
    :status 400: Invalid request. Check response data for details. This can happen when an invalid ``old_password`` is provided, or if ``new_password`` fails the password validation checks.


------------------
Email Verification
------------------

Before a user can log in, they must have a verified email address. This allows us to contact the user with any account related messages.

.. note::

    We require the user's password to prevent mistyped email addresses from being verified by an unknown user. See :issue:`39` for details.

.. http:post:: /account/verify-email/

    Verify an email address.

    :<json string key: The confirmation key that was sent to the user's email.
    :<json string password: The user's password.

    :status 200: The email address was confirmed.
    :status 400: Invalid request. Check the response data for details. This can happen if an invalid key was provided, or if the key has expired.


----------------
Email Management
----------------

Users are allowed to have multiple emails associated with their account. One of these emails is the user's primary address, and receives all notifications. The user can log in with any of their verified emails.

Email List
----------

The email list endpoint allows for listing of a user's email addresses as well as adding new emails.

.. http:get:: /account/emails/

    List the requesting user's email addresses.

    :>jsonarr int id: The ID of the email address.
    :>jsonarr string email: The email's address.
    :>jsonarr boolean verified: A boolean indicating if the address has been verified.
    :>jsonarr boolean primary: A boolean indicating if the address is the user's primary email.

    :status 200: The user's email addresses were successfully retrieved.

.. http:post:: /account/emails/

    Add a new email address for the requesting user.

    :<json string email: The address of the new email.

    :>header Location: The URL of the created email address' detail view.

    :>json int id: The ID of the email address.
    :>json string url: The URL of the email address' detail view.
    :>json string email: The email's address.
    :>json boolean verified: A boolean indicating if the address has been verified.
    :>json boolean primary: A boolean indicating if the address is the user's primary email.

    :status 201: The email address was created successfully.
    :status 400: Invalid request. Check the response data for details.

Email Detail
------------

The email detail endpoint allows for retrieving and updating a specific email address as well as removing email addresses.

.. http:get:: /account/emails/(int:id)/

    Get the details of a specific email address.

    :>json int id: The ID of the email address.
    :>json string url: The URL of the email address' detail view.
    :>json string email: The email's address.
    :>json boolean verified: A boolean indicating if the address has been verified.
    :>json boolean primary: A boolean indicating if the address is the user's primary email.

    :status 200: The email address' details were successfully retrieved.
    :status 404: There is no email address with the given ``id`` accessible to
    the requesting user.

.. http:patch:: /account/emails/(int:id)/

    Update the details of a specific email address.

    :<json boolean primary: *(Optional)* A boolean indicating if the specified email address should be the user's new primary email.

    :>json int id: The ID of the email address.
    :>json string url: The URL of the email address' detail view.
    :>json string email: The email's address.
    :>json boolean verified: A boolean indicating if the address has been verified.
    :>json boolean primary: A boolean indicating if the address is the user's primary email.

    :status 200: The email address' details were successfully updated.
    :status 404: There is no email address with the given ``id`` accessible to
    the requesting user.

.. http:delete:: /account/emails/(int:id)/

    Delete a specific email address.

    :status 204: The email address was successfully deleted.
    :status 404: There is no email address with the given ``id`` accessible to the requesting user.
    :status 409: The email address is the user's primary address so it could not be deleted.
