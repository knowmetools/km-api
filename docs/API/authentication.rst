.. _api-authentication:

==============
Authentication
==============


------------
Registration
------------

In order to log in, you must have a user account. User accounts can be created by sending a ``POST`` request to the registration endpoint.

.. http:post:: /auth/register/

    Register a new user.

    :<json string email: The email address to register the user under.
    :<json string password: The password to give the new user.
    :<json string first_name: The user's first name.
    :<json string last_name: The user's last name.

    :>json int id: The new user's ID.
    :>json string email: The new user's email address.
    :>json string first_name: The new user's first name.
    :>json string last_name: The new user's last name.

    :statuscode 201: A new user was sucessfully created.
    :statuscode 400: Bad request; check response for details.
    :statuscode 403: Authentication credentials were provided. This endpoint requires the user to be unauthenticated.


-----
Login
-----

Logging in will return a token that can be used to authenticate with other
endpoints.

.. http:post:: /auth/login/

    Log in an existing user.

    :<json string username: The user's email address.
    :<json string password: The user's password.

    :>json string token: A token the user can use to authenticate with the API.

    :statuscode 200: User sucessfully authenticated.
    :statuscode 400: The provided credentials were invalid.


------------
User Profile
------------

We store basic information about each user (provided when they register) that can be retrieved or updated from this endpoint.

.. http:get:: /auth/profile/

    Retrieve a user's information.

    :>json int id: The user's ID.
    :>json string email: The user's email address.
    :>json string first_name: The user's first name.
    :>json string last_name: The user's last name.

    :statuscode 200: Request was successful.

.. http:patch:: /auth/profile/

    Update a user's profile.

    :>json string email: *(Optional)* The user's new email address.
    :>json string first_name: *(Optional)* The user's new first name.
    :>json string last_name: *(Optional)* The user's new last name.

    :statuscode 200: Successfully updated the user's information.
    :statuscode 400: Invalid request. Check the response data for details.


-----
Layer
-----

For real time communications we use Layer_. Layer requires an identity token in order to authenticate with their services.

.. http:post:: /auth/layer/

    Obtain an identity token for Layer.

    :<json string nonce: A `nonce <layer-nonce_>`_ from Layer.

    :>json string identity_token: An `identity token <layer-identity-token_>`_ for Layer.

    :statuscode 201: Identity token successfully created.
    :statuscode 400: Invalid request. Check the response data for details.

.. warning::

    Just because an identity token was received does not mean the identity token is valid. If an invalid nonce was provided, the returned token will also be invalid.


.. _Layer: https://layer.com/
.. _layer-identity-token: https://docs.layer.com/reference/client_api/authentication.out#identity-token
.. _layer-nonce: https://docs.layer.com/reference/client_api/authentication.out
