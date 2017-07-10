=======
Account
=======


---------------
Change Password
---------------

.. http:post:: /account/change-password/

    Change the password of the currently authenticated user.

    :<json string old_password: The user's current password.
    :<json string new_password: The user's new password.

    :status 200: The user's password was successfully changed.
    :status 400: Invalid request. Check response data for details. This can happen when an invalid ``old_password`` is provided, or if ``new_password`` fails the password validation checks.
