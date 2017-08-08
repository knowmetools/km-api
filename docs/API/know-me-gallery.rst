=================
Know Me - Gallery
=================

The gallery is used to store various files associated with a know me user. Media resources (items in the gallery) can be attached to a particular profile item.

.. note::

    Currently there is no way to retrieve media resources that are not attached to a profile item. This will be introduced later as a paid feature.


------------
Gallery View
------------

This endpoint allows for creation of new media resources.

.. http:post:: /know-me/users/(int:id)/gallery/

    Create a new media resource.

    .. note::

        Since media resources involve a file, the request be sent with the header ``Content-Type: multipart/form-data``.

    :param int id: The ID of the know me user to create a media resource for.

    :form string name: The name to give the file being uploaded.
    :form file file: The file to upload.

    :>header Location: The URL of the created media resource's detail view.

    :>json int id: The ID of the created media resource.
    :>json string url: The URL of the created media resource's detail view.
    :>json string name: The name the media resource was created with.
    :>json string file: The URL of the file attached to the media resource.

    :status 201: The media resource was succesfully created.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no know me user with the given ``id`` accessible to the requesting user.


-----------------
Media Resource View
-----------------

This endpoint allows for retrieving and updating a specific media resource's information.

.. http:get:: /know-me/media-resources/(int:id)/

    Get the information of a specific media resource.

    :param int id: The ID of the media resource to retrieve.

    :>json int id: The ID of the media resource.
    :>json string url: The URL of the media resource's detail view.
    :>json string name: The name of the media resource.
    :>json string file: The URL of the file attached to the media resource.

    :status 200: The media resource's information was succesfully retrieved.
    :status 404: There is no media resource with the given ``id`` accessible to the requesting user.

.. http:patch:: /know-me/media-resources/(int:id)/

    Update a specific media resource's information.

    :param int id: The ID of the media resource to update.

    :<form string name: *(Optional)* A new name for the media resource.
    :<form file file: *(Optional)* A new file to associate with the media resource.

    :status 200: The media resource was succesfully updated.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no media resource with the given ``id`` accessible to the requesting user.
