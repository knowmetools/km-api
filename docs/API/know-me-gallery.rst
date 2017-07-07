=================
Know Me - Gallery
=================

The gallery is used to store various files associated with a profile. Items in the gallery can be attached to a particular profile item.

.. note::

    Currently there is no way to retrieve gallery items that are not attached to a profile item. This will be introduced later as a paid feature.


------------
Gallery View
------------

This endpoint allows for creation of new gallery items.

.. http:post:: /know-me/profiles/(int:id)/gallery/

    Create a new gallery item.

    .. note::

        Since gallery items involve a file, the request be sent with the header ``Content-Type: multipart/form-data``.

    :param int id: The ID of the profile to create a gallery item for.

    :form string name: The name to give the file being uploaded.
    :form file resource: The file to upload.

    :>header Location: The URL of the created gallery item's detail view.

    :>json int id: The ID of the created gallery item.
    :>json string url: The URL of the created gallery item's detail view.
    :>json string name: The name the gallery item was created with.
    :>json string resource: The URL of the file attached to the gallery item.

    :status 201: The gallery item was succesfully created.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no profile with the given ``id`` accessible to the requesting user.


-----------------
Gallery Item View
-----------------

This endpoint allows for retrieving and updating a specific gallery item's information.

.. http:get:: /know-me/gallery-items/(int:id)/

    Get the information of a specific gallery item.

    :param int id: The ID of the gallery item to retrieve.

    :>json int id: The ID of the gallery item.
    :>json string url: The URL of the gallery item's detail view.
    :>json string name: The name of the gallery item.
    :>json string resource: The URL of the file attached to the gallery item.

    :status 200: The gallery item's information was succesfully retrieved.
    :status 404: There is no gallery item with the given ``id`` accessible to the requesting user.

.. http:patch:: /know-me/gallery-items/(int:id)/

    Update a specific gallery item's information.

    :param int id: The ID of the gallery item to update.

    :<form string name: *(Optional)* A new name for the gallery item.
    :<form file resource: *(Optional)* A new file to associate with the gallery item.

    :status 200: The gallery item was succesfully updated.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no gallery item with the given ``id`` accessible to the requesting user.
