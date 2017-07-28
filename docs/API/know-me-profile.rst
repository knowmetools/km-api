=================
Know Me - Profile
=================

These endpoints provide data for the Know Me app.


--------
Profiles
--------

Profiles are the basis of Know Me. They contain organized sets of information about a specific user.

Profile List
------------

.. http:get:: /know-me/profiles/

    Get the list of profiles that the requesting user has access to.

    :>jsonarr int id: The profile's ID.
    :>jsonarr string url: The URL of the profile's detail view.
    :>jsonarr string name: The name of the profile.
    :>jsonarr string quote: A quote from the user who owns the profile.
    :>jsonarr string welcome_message: A message welcoming other users to the profile.

    :statuscode 200: The request was successful.

.. http:post:: /know-me/profiles/

    Create a new profile for the user making the request.

    :<json string name: A name for the profile.
    :<json string quote: A quote from the user.
    :<json string welcome_message: A message welcoming other people to the profile.

    :>header Location: The URL of the created profile's detail view.

    :>json int id: The profile's ID.
    :>json string url: The URL of the profile's detail view.
    :>json string name: The name of the profile.
    :>json string quote: A quote from the user who owns the profile.
    :>json string welcome_message: A message welcoming other users to the profile.

    :statuscode 201: The new profile was successfully created.
    :statuscode 400: Invalid request. Check the response data for details.

.. note::

    Currently, a user may only have one profile.

Profile Details
---------------

.. http:get:: /know-me/profiles/(int:id)/

    Get the details of a specific profile.

    :param id: The ID of the profile to get.

    :>json int id: The profile's ID.
    :>json string url: The URL of the profile's detail view.
    :>json string name: The name of the profile.
    :>json string quote: A quote from the user who owns the profile.
    :>json string welcome_message: A message welcoming other users to the profile.
    :>json string gallery_url: The URL of the profile's gallery.
    :>json string groups_url: The URL of the profile's group list.
    :>json array groups: A list of the groups contained in the profile.

    :statuscode 200: The profile's details were retrieved succesfully.
    :statuscode 404: There is no profile with the given `id` accessible to the requesting user.

.. http:patch:: /know-me/profiles/(int:id)/

    Update a specific profile's details.

    :param id: The ID of the profile to update.

    :<json string name: *(Optional)* The profile's new name.
    :<json string quote: *(Optional)* The profile's new quote.
    :<json string welcome_message: *(Optional)* The profile's new welcome message.

    :>json int id: The profile's ID.
    :>json string url: The URL of the profile's detail view.
    :>json string name: The name of the profile.
    :>json string quote: A quote from the user who owns the profile.
    :>json string welcome_message: A message welcoming other users to the profile.
    :>json string gallery_url: The URL of the profile's gallery.
    :>json string groups_url: The URL of the profile's group list.
    :>json array groups: A list of the groups contained in the profile.

    :statuscode 200: The profile's details were succesfully updated.
    :statuscode 400: The update failed. Check the response data for details.


--------------
Profile Groups
--------------

Profile groups are the next step down in a profile. They contain information targeted towards a group of people.

Profile Group List
------------------

The profile group list endpoint allows for listing of a profile's groups as well as creation of new profile groups.

.. http:get:: /know-me/profiles/(int:id)/groups/

    List the groups in a particular profile.

    :param int id: The ID of the profile to fetch the groups of.

    :>jsonarr int id: The ID of the profile group.
    :>jsonarr string url: The URL of the profile group's detail view.
    :>jsonarr string name: The name of the profile group.
    :>jsonarr boolean is_default: A boolean representing if the group is the default for its profile.

    :statuscode 200: The profile's groups were retrieved succesfully.
    :statuscode 404: No profile with the given `id` was found.

.. http:post:: /know-me/profiles/(int:id)/groups/

    Create a new profile group for the given profile.

    :param int id: The ID of the profile to create a group for.

    :<json string name: The name of the profile group.
    :<json boolean is_default: *(Optional)* A boolean determining if the group will be the default group for the profile. Defaults to ``false``.

    :>header Location: The URL of the created profile group's detail view.

    :>json int id: The ID of the profile group.
    :>json string url: The URL of the profile group's detail view.
    :>json string name: The name of the profile group.
    :>json boolean is_default: A boolean representing if the group is the default for its profile.

    :statuscode 201: The profile group was successfully created.
    :statuscode 400: Invalid request. Check the response data for details.

Profile Group Detail
--------------------

The profile group detail endpoint allows for viewing and updating a profile group's information.

.. http:get:: /know-me/groups/(int:id)/

    Get the details of a particular profile group.

    :param int id: The ID of the profile group to fetch.

    :>json int id: The ID of the profile group.
    :>json string url: The URL of the profile group's detail view.
    :>json string name: The name of the profile group.
    :>json boolean is_default: A boolean representing if the group is the default for its profile.
    :>json string rows_url: The URL of the group's row list.
    :>json array rows: A list of the profile rows contained in the group.

    :status 200: The profile group's details were retrieved succesfully.
    :status 404: There is no profile group with the given ``id`` accessible to the requesting user.

.. http:patch:: /know-me/groups/(int:id)/

    Update a specific profile group's information.

    :param int id: The ID of the profile group to update.

    :<json string name: *(Optional)* A new name for the profile group.
    :<json boolean is_default: *(Optional)* The new ``is_default`` status for the group.

    :>json int id: The ID of the profile group.
    :>json string url: The URL of the profile group's detail view.
    :>json string name: The name of the profile group.
    :>json boolean is_default: A boolean representing if the group is the default for its profile.
    :>json string rows_url: The URL of the group's row list.
    :>json array rows: A list of the profile rows contained in the group.

    :status 200: The profile group's information was succesfully updated.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no profile group with the given ``id`` accessible to the requesting user.


------------
Profile Rows
------------

Profile rows hold specific categories of information for a profile group.

Profile Row List
----------------

.. http:get:: /know-me/groups/(int:id)/rows/

    List the rows in a particular profile group.

    :param int id: The ID of the profile group to fetch the rows of.

    :>jsonarr int id: The ID of the row.
    :>jsonarr string url: The URL of the row's detail view.
    :>jsonarr string name: The name of the row.
    :>jsonarr int row_type: An integer representing the type of the row.
    :>jsonarr string items_url: The URL of the row's item list.
    :>jsonarr array items: The items contained in the row.

    :status 200: The profile row list was succesfully retrieved.
    :status 404: There is no profile group with the given ``id`` accessible to the requesting user.

.. http:post:: /know-me/groups/(int:id)/rows/

    Create a new profile row in a particular group.

    :param int id: The ID of the profile group to create a row for.

    :<json string name: A name for the row.
    :<json int row_type: An integer representing which type of row to create.

    :>header Location: The URL of the created row's detail view.

    :>json int id: The ID of the row.
    :>json string url: The URL of the row's detail view.
    :>json string name: The name of the row.
    :>json int row_type: An integer representing the type of row.
    :>json string items_url: The URL of the row's item list.
    :>json array items: The items contained in the row.

    :status 201: The profile row was succesfully created.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no profile group with the given ``id`` accessible to the requesting user.

Profile Row Detail
------------------

This endpoint allows for viewing and updating a specific profile row's information.

.. http:get:: /know-me/rows/(int:id)/

    Get a specific profile row's information.

    :param int id: The ID of the profile row to fetch.

    :>json int id: The ID of the row.
    :>json string url: The URL of the row's detail view.
    :>json string name: The name of the row.
    :>json int row_type: An integer representing the type of row.
    :>json string items_url: The URL of the row's item list.
    :>json array items: The items contained in the row.

    :status 200: The profile row's information was succesfully retrieved.
    :status 404: There is no profile row with the given ``id`` accessible to the requesting user.

.. http:patch:: /know-me/rows/(int:id)/

    Update a specific profile row's details.

    :param int id: The ID of the row to update.

    :<json string name: *(Optional)* A new name for the row.
    :<json int row_type: *(Optional)* The row's new type, as an integer.

    :>json int id: The ID of the row.
    :>json string url: The URL of the row's detail view.
    :>json string name: The name of the row.
    :>json int row_type: An integer representing the type of row.
    :>json string items_url: The URL of the row's item list.
    :>json array items: The items contained in the row.

    :status 200: The profile row's information was succesfully updated.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no profile row with the given ``id`` accessible to the requesting user.


-------------
Profile Items
-------------

Profile items contain specific pieces of the information in a profile row.

Profile Item List
-----------------

This endpoint allows for listing the items in a profile row and adding new items to the row.

.. http:get:: /know-me/rows/(int:id)/items/

    List the items in a profile row.

    :param int id: The ID of the profile row to fetch the items for.

    :>jsonarr int id: The ID of the item.
    :>jsonarr string url: The URL of the item's detail view.
    :>jsonarr string name: The name of the item.
    :>jsonarr string text: The text the item contains.
    :>jsonarr int media_resource: The ID of the media resource attached to the profile item. Not present if the profile item doesn't have an attached media resource.
    :>jsonarr object media_resource_info: The attached media resource's information, if present.

    :status 200: The profile item list was succesfully retrieved.
    :status 404: There is no profile row with the given ``id`` accessible to the requesting user.

.. http:post:: /know-me/rows/(int:id)/items/

    Create a new profile item in a particular row.

    :param int id: The ID of the profile row to create an item in.

    :<json string name: The name of the item.
    :<json string text: The text the item will contain.
    :<json int media_resource: *(Optional)* The ID of a media resource to attach to the profile item.

    :>header Location: The URL of the created item's detail view.

    :>json int id: The ID of the item.
    :>json string url: The URL of the item's detail view.
    :>json string name: The name of the item.
    :>json string text: The text the item contains.
    :>json int media_resource: The ID of the media resource attached to the profile item. Not present if the profile item doesn't have an attached media resource.
    :>json object media_resource_info: The attached media resource's information, if present.

    :status 201: The profile item was succesfully created.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no profile row with the given ``id`` accessible to the requesting user.

Profile Item Detail
-------------------

This endpoint allows for retrieving and updating a specific profile item's information.

.. http:get:: /know-me/items/(int:id)/

    Retrieve a specific profile item's information.

    :param int id: The ID of the profile item to fetch.

    :>json int id: The ID of the item.
    :>json string url: The URL of the item's detail view.
    :>json string name: The name of the item.
    :>json string text: The text the item contains.
    :>json int media_resource: The ID of the media resource attached to the profile item. Not present if the profile item doesn't have an attached media resource.
    :>json object media_resource_info: The attached media resource's information, if present.

    :status 200: The profile item's information was succesfully retrieved.
    :status 404: There is no profile item with the given ``id`` accessible to the requesting user.

.. http:patch:: /know-me/items/(int:id)/

    Update a specific profile item's information.

    :param int id: The ID of the profile item to update.

    :<json string name: *(Optional)* A new name for the item.
    :<json string text: *(Optional)* New text for the item.

    :>json int id: The ID of the item.
    :>json string url: The URL of the item's detail view.
    :>json string name: The name of the item.
    :>json string text: The text the item contains.
    :>json int media_resource: The ID of the media resource attached to the profile item. Not present if the profile item doesn't have an attached media resource.
    :>json object media_resource_info: The attached media resource's information, if present.

    :status 200: The profile item's information was succesfully updated.
    :status 404: There is no profile item with the given ``id`` accessible to the requesting user.
