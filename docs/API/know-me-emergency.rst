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
    :>jsonarr string name: The emergency item's name.
    :>jsonarr string description: The emergency item's description. Can be an empty string.
    :>jsonarr object media_resource: The media resource associated with the emergency item. Can be ``null``.

    :status 200: The emergency item list was succesfully retrieved.
    :status 404: There is no Know Me user with the provided ``id`` accessible to the requesting user.
