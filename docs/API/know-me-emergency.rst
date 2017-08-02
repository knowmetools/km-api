===================
Know Me - Emergency
===================

Know Me provides a way for users to store some information about themselves that could be used in case of an emergency.


---------------
Emergency Items
---------------

Emergency items are similar to profile items, but they are meant to store information for emergency situations.

Emergency Item List
-------------------

The emergency item list endpoint allows for listing and creation of emergency items.

.. http:get:: /know-me/users/(int:id)/emergency-items/

    List the emergency items for a Know Me user.

    :>jsonarr int id: The emergency item's ID.
    :>jsonarr string url: The URL of the emergency item's detail view.
    :>jsonarr string name: The emergency item's name.
    :>jsonarr string description: The emergency item's description. Can be an empty string.
    :>jsonarr object media_resource: The media resource associated with the emergency item. Can be ``null``.

    :status 200: The emergency item list was successfully retrieved.
    :status 404: There is no Know Me user with the provided ``id`` accessible to the requesting user.

.. http:post:: /know-me/users/(int:id)/emergency-items/

    Create a new emergency item.

    :<json string name: The emergency item's name.
    :<json string description: *(Optional)* The emergency item's description.
    :<json int media_resource: *(Optional)* The ID of a media resource to attach to the emergency item.

    :>header Location: The URL of the created emergency item's detail view.

    :>json int id: The emergency item's ID.
    :>json string url: The URL of the emergency item's detail view.
    :>json string name: The emergency item's name.
    :>json string description: The emergency item's description. This can be an empty string.
    :>json object media_resource: The media resource attached to the item. This can be ``null``.

    :status 200: A new emergency item was successfully created.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no Know Me user with the provided ``id`` accessible to the requesting user.

Emergency Item Detail
---------------------

The emergency item detail endpoint allows for retrieving, updating, or deleting of specific emergency items.

.. http:get:: /know-me/emergency-items/(int:id)/

    Retrieve a specific emergency item's details.

    :>json int id: The emergency item's ID.
    :>json string url: The URL of the emergency item's detail view.
    :>json string name: The emergency item's name.
    :>json string description: The emergency item's description. This can be an empty string.
    :>json object media_resource: The media resource attached to the item. This can be ``null``.

    :status 200: The emergency item's details were successfully retrieved.
    :status 404: There is no emergency item with the provided ``id`` accessible to the requesting user.

.. http:patch:: /know-me/emergency-items/(int:id)/

    Update a particular emergency item.

    :<json string name: *(Optional)* A new name for the item.
    :<json string description: *(Optional)* A new description for the item.
    :<json int media_resource: *(Optional)* The ID of a media resource to attach to the item.

    :>json int id: The emergency item's ID.
    :>json string url: The URL of the emergency item's detail view.
    :>json string name: The emergency item's name.
    :>json string description: The emergency item's description. This can be an empty string.
    :>json object media_resource: The media resource attached to the item. This can be ``null``.

    :status 200: The emergency item's details were successfully updated.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no emergency item with the provided ``id`` accessible to the requesting user.

.. http:delete:: /know-me/emergency-items/(int:id)/

    Delete a particular emergency item.

    :status 204: The emergency item was successfully deleted.
    :status 404: There is no emergency item with the provided ``id`` accessible to the requesting user.
