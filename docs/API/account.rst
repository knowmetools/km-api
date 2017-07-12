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

    :<json string email: *(Optional)* The user's new email address.
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

.. http:post:: /account/verify-email/

    Verify an email address.

    :<json string key: The confirmation key that was sent to the user's email.

    :status 200: The email address was confirmed.
    :status 400: Invalid request. Check the response data for details. This can happen if an invalid key was provided, or if the key has expired.
