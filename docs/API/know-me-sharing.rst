=================
Know Me - Sharing
=================

Know Me supports sharing of profiles with other users. The account owner can invite other users to view their profiles with varying levels of access.


---------
Accessors
---------

Sharing is granted through the creation of ``Accessors`` which grant a user with a specific email address access to a user's profiles.

Accessor List View
------------------

The accessor list view allows for retrieving existing accessors and creating new ones.

.. http:get:: /know-me/users/accessors/

    List the existing accessors for the requesting user.

    :>jsonarr boolean accepted: A boolean indicating if the invitation has been accepted by the invited user.
    :>jsonarr boolean can_write: A boolean indicating if the accessor grants the invited user write access to profiles.
    :>jsonarr string email: The email address used to invite the user.
    :>jsonarr boolean has_private_profile_access: A boolean indicating if the accessor grants the user access to profiles marked as private.
    :>jsonarr object km_user: An object containing information about the user that the accessor grants access on.

    :status 200: Request successful.

.. http:post:: /know-me/users/accessors/

    Create a new accessor for the requesting user's account.

    :<json boolean can_write: A boolean indicating if the invited user should have write access for shared profiles.
    :<json string email: The email address of the user to invite.
    :<json boolean has_private_profile_access: A boolean indicating if the invited user should have access to profiles marked as private.

    :>json boolean accepted: A boolean indicating if the invitation has been accepted by the invited user.
    :>json boolean can_write: A boolean indicating if the accessor grants the invited user write access to profiles.
    :>json string email: The email address used to invite the user.
    :>json boolean has_private_profile_access: A boolean indicating if the accessor grants the user access to profiles marked as private.
    :>json object km_user: An object containing information about the user that the accessor grants access on.

    :status 201: The accessor was created successfully.
    :status 400: Invalid request. Check the response data for details.

Accessor Detail View
--------------------

The accessor detail view allows for retrieving, updating, or deleting a specific acccessor.

.. http:get:: /know-me/accessors/(int:id)/

    Retrieve the details of a specific accessor.

    :param int id: The ID of the accessor to retrieve.

    :>json boolean accepted: A boolean indicating if the invitation has been accepted by the invited user.
    :>json boolean can_write: A boolean indicating if the accessor grants the invited user write access to profiles.
    :>json string email: The email address used to invite the user.
    :>json boolean has_private_profile_access: A boolean indicating if the accessor grants the user access to profiles marked as private.
    :>json object km_user: An object containing information about the user that the accessor grants access on.

    :status 200: Request successful.
    :status 404: There is no accessor with the provided ``id``.

.. http:patch:: /know-me/accessors/(int:id)/

    Update a specific accessor's information.

    :param int id: The ID of the accessor to update.

    :<json boolean can_write: *(Optional)* A boolean indicating if the invited user has write access to profiles.
    :<json boolean has_private_profile_access: *(Optional)* A boolean indicating if the invited user has access to profiles marked as private.

    :status 200: Request successful.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no accessor with the provided ``id``.

.. http:delete:: /know-me/accessors/(int:id)/

    Delete a specific accessor.

    :param int id: The ID of the accessor to delete.

    :status 204: Request successful.
    :status 404: There is no accessor with the provided ``id``.

Pending Accessor List View
--------------------------

This view allows listing of the accessors that have not yet been accepted by
the user the accessor grants access to.

.. http:get:: /know-me/accessors/pending/

    Get the pending accessors for the requesting user.

    :>jsonarr can_write accepted: A boolean indicating if the accessor has been accepted yet. This will be ``false`` for all elements in the list.
    :>jsonarr boolean can_write: A boolean indicating if the accessor grants the user write permission on the shared profiles.
    :>jsonarr string email: The email address used to invite the user.
    :>jsonarr boolean has_private_profile_access: A boolean indicating if the accessor grants access to profiles marked as private.
    :>jsonarr object km_user: An object containing details about the Know Me user the accessor grants access to.

    :status 200: The request was successful.
