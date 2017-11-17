==================
Know Me - Profiles
==================

These endpoints provide data for the Know Me app.


-------------
Know Me Users
-------------

Know Me users accounts hold data specific to the Know Me app.

Know Me User List
-----------------

.. http:get:: /know-me/users/

    Get the list of know me users that the requesting user has access to.

    :>jsonarr int id: The know me user's ID.
    :>jsonarr string url: The URL of the know me user's detail view.
    :>jsonarr string name: The name of the know me user.
    :>jsonarr string quote: A quote from the user who owns the know me user.

    :statuscode 200: The request was successful.

.. http:post:: /know-me/users/

    Create a new know me user for the user making the request.

    :<json string name: A name for the know me user.
    :<json string quote: A quote from the user.

    :>header Location: The URL of the created know me user's detail view.

    :>json int id: The know me user's ID.
    :>json string url: The URL of the know me user's detail view.
    :>json string name: The name of the know me user.
    :>json string quote: A quote from the user who owns the know me user.

    :statuscode 201: The new know me user was successfully created.
    :statuscode 400: Invalid request. Check the response data for details.

.. note::

    Currently, a user may only have one know me user.

Know Me User Details
--------------------

.. http:get:: /know-me/profiles/(int:id)/

    Get the details of a specific know me user.

    :param id: The ID of the know me user to get.

    :>json int id: The know me user's ID.
    :>json string url: The URL of the know me user's detail view.
    :>json string name: The name of the know me user.
    :>json string quote: A quote from the user who owns the know me user.
    :>json string emergency_items_url: The URL of the user's emergency item list.
    :>json string gallery_url: The URL of the know me user's gallery.
    :>json string profiles_url: The URL of the know me user's profile list.
    :>json array profiles: A list of the profiles contained in the know me user.

    :statuscode 200: The know me user's details were retrieved succesfully.
    :statuscode 404: There is no know me user with the given `id` accessible to the requesting user.

.. http:patch:: /know-me/profiles/(int:id)/

    Update a specific know me user's details.

    :param id: The ID of the know me user to update.

    :<json string name: *(Optional)* The know me user's new name.
    :<json string quote: *(Optional)* The know me user's new quote.

    :>json int id: The know me user's ID.
    :>json string url: The URL of the know me user's detail view.
    :>json string name: The name of the know me user.
    :>json string quote: A quote from the user who owns the know me user.
    :>json string emergency_items_url: The URL of the know me user's emergency item list.
    :>json string gallery_url: The URL of the know me user's gallery.
    :>json string profiles_url: The URL of the know me user's profile list.
    :>json array profiles: A list of the profiles contained in the know me user.

    :statuscode 200: The know me user's details were succesfully updated.
    :statuscode 400: The update failed. Check the response data for details.


--------
Profiles
--------

Profiles are the next step down in a know me user. They contain information targeted towards a profile of people.

Profile List
------------

The profile list endpoint allows for listing of a know me user's profiles as well as creation of new profiles.

.. http:get:: /know-me/users/(int:id)/profiles/

    List the profiles in a particular know me user.

    :param int id: The ID of the know me user to fetch the profiles of.

    :>jsonarr int id: The ID of the profile.
    :>jsonarr string url: The URL of the profile's detail view.
    :>jsonarr string name: The name of the profile.
    :>jsonarr boolean is_default: A boolean representing if the profile is the default for its know me user.

    :statuscode 200: The know me user's profiles were retrieved succesfully.
    :statuscode 404: No know me user with the given `id` was found.

.. http:post:: /know-me/users/(int:id)/profiles/

    Create a new profile for the given know me user.

    :param int id: The ID of the know me user to create a profile for.

    :<json string name: The name of the profile.
    :<json boolean is_default: *(Optional)* A boolean determining if the profile will be the default profile for the know me user. Defaults to ``false``.

    :>header Location: The URL of the created profile's detail view.

    :>json int id: The ID of the profile.
    :>json string url: The URL of the profile's detail view.
    :>json string name: The name of the profile.
    :>json boolean is_default: A boolean representing if the profile is the default for its know me user.

    :statuscode 201: The profile was successfully created.
    :statuscode 400: Invalid request. Check the response data for details.

Profile Detail
--------------

The profile detail endpoint allows for viewing and updating a profile's information.

.. http:get:: /know-me/profiles/(int:id)/

    Get the details of a particular profile.

    :param int id: The ID of the profile to fetch.

    :>json int id: The ID of the profile.
    :>json string url: The URL of the profile's detail view.
    :>json string name: The name of the profile.
    :>json boolean is_default: A boolean representing if the profile is the default for its know me user.
    :>json string topics_url: The URL of the profile's topic list.
    :>json array topics: A list of the profile topics contained in the profile.

    :status 200: The profile's details were retrieved succesfully.
    :status 404: There is no profile with the given ``id`` accessible to the requesting user.

.. http:patch:: /know-me/profiles/(int:id)/

    Update a specific profile's information.

    :param int id: The ID of the profile to update.

    :<json string name: *(Optional)* A new name for the profile.
    :<json boolean is_default: *(Optional)* The new ``is_default`` status for the profile.

    :>json int id: The ID of the profile.
    :>json string url: The URL of the profile's detail view.
    :>json string name: The name of the profile.
    :>json boolean is_default: A boolean representing if the profile is the default for its know me user.
    :>json string topics_url: The URL of the profile's topic list.
    :>json array topics: A list of the know me user topics contained in the profile.

    :status 200: The profile's information was succesfully updated.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no profile with the given ``id`` accessible to the requesting user.


--------------
Profile Topics
--------------

Profile topics hold specific categories of information for a profile.

Profile Topic List
------------------

.. http:get:: /know-me/profiles/(int:id)/topics/

    List the topics in a particular profile.

    :param int id: The ID of the profile to fetch the topics of.

    :>jsonarr int id: The ID of the topic.
    :>jsonarr string url: The URL of the topic's detail view.
    :>jsonarr string name: The name of the topic.
    :>jsonarr int topic_type: An integer representing the type of the topic.
    :>jsonarr string items_url: The URL of the topic's item list.
    :>jsonarr array items: The items contained in the topic.

    :status 200: The profile topic list was succesfully retrieved.
    :status 404: There is no profile with the given ``id`` accessible to the requesting user.

.. http:post:: /know-me/profiles/(int:id)/topics/

    Create a new profile topic in a particular profile.

    :param int id: The ID of the profile to create a topic for.

    :>jsonarr string topics_url: The URL of the given topic's list.
    :>jsonarr object topics: An object containing the profile's topic.
    :<json string name: A name for the topic.
    :<json int topic_type: An integer representing which type of topic to create.

    :>header Location: The URL of the created topic's detail view.

    :>json int id: The ID of the topic.
    :>json string url: The URL of the topic's detail view.
    :>json string name: The name of the topic.
    :>json int topic_type: An integer representing the type of topic. The choices are:

        * ``3`` -- Text topic
        * ``4`` -- Visual topic

    :>json string items_url: The URL of the topic's item list.
    :>json array items: The items contained in the topic.

    :status 201: The profile topic was succesfully created.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no profile with the given ``id`` accessible to the requesting user.

Profile Topic Detail
--------------------

This endpoint allows for viewing and updating a specific profile topic's information.

.. http:get:: /know-me/topics/(int:id)/

    Get a specific profile topic's information.

    :param int id: The ID of the profile topic to fetch.

    :>json int id: The ID of the topic.
    :>json string url: The URL of the topic's detail view.
    :>json string name: The name of the topic.
    :>json int topic_type: An integer representing the type of topic.
    :>json string items_url: The URL of the topic's item list.
    :>json array items: The items contained in the topic.

    :status 200: The profile topic's information was succesfully retrieved.
    :status 404: There is no profile topic with the given ``id`` accessible to the requesting user.

.. http:patch:: /know-me/topics/(int:id)/

    Update a specific profile topic's details.

    :param int id: The ID of the topic to update.

    :<json string name: *(Optional)* A new name for the topic.
    :<json int topic_type: *(Optional)* The topic's new type, as an integer.

    :>json int id: The ID of the topic.
    :>json string url: The URL of the topic's detail view.
    :>json string name: The name of the topic.
    :>json int topic_type: An integer representing the type of topic.
    :>json string items_url: The URL of the topic's item list.
    :>json array items: The items contained in the topic.

    :status 200: The profile topic's information was succesfully updated.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no profile topic with the given ``id`` accessible to the requesting user.


-------------
Profile Items
-------------

Profile items contain specific pieces of the information in a profile topic.

Profile Item List
-----------------

This endpoint allows for listing the items in a profile topic and adding new items to the topic.

.. http:get:: /know-me/topics/(int:id)/items/

    List the items in a profile topic.

    :param int id: The ID of the profile topic to fetch the items for.

    :>jsonarr int id: The ID of the item.
    :>jsonarr string url: The URL of the item's detail view.
    :>jsonarr string name: The name of the item.
    :>jsonarr object image_content: An object containing the item's image content. May be ``null``.
    :>jsonarr object list_content: An object containing the item's list content. May be ``null`.

    :status 200: The profile item list was succesfully retrieved.
    :status 404: There is no profile topic with the given ``id`` accessible to the requesting user.

.. http:post:: /know-me/topics/(int:id)/items/

    Create a new profile item in a particular topic.

    :param int id: The ID of the profile topic to create an item in.

    :<json string name: The name of the item.
    :<json object image_content: An object containing the item's image content. Mutually exclusive with ``list_content``.
    :<json object list_content: An object containing the item's list content. Mutually exclusive with ``image_content``.

    :>header Location: The URL of the created item's detail view.

    :>json int id: The ID of the item.
    :>json string url: The URL of the item's detail view.
    :>json string name: The name of the item.
    :>json object image_content: An object containing the item's image content. May be ``null``.
    :>json object list_content: An object containing the item's list content. May be ``null`.

    :status 201: The profile item was succesfully created.
    :status 400: Invalid request. Check the response data for details.
    :status 404: There is no profile topic with the given ``id`` accessible to the requesting user.

Profile Item Detail
-------------------

This endpoint allows for retrieving and updating a specific profile item's information.

.. http:get:: /know-me/items/(int:id)/

    Retrieve a specific profile item's information.

    :param int id: The ID of the profile item to fetch.

    :>json int id: The ID of the item.
    :>json string url: The URL of the item's detail view.
    :>json string name: The name of the item.
    :>json object image_content: An object containing the item's image content. May be ``null``.
    :>json object list_content: An object containing the item's list content. May be ``null`.

    :status 200: The profile item's information was succesfully retrieved.
    :status 404: There is no profile item with the given ``id`` accessible to the requesting user.

.. http:patch:: /know-me/items/(int:id)/

    Update a specific profile item's information.

    :param int id: The ID of the profile item to update.

    :<json string name: *(Optional)* A new name for the item.
    :>json object image_content: *(Optional)* An object containing the item's image content. May be ``null``.
    :>json object list_content: *(Optional)* An object containing the item's list content. May be ``null`.

    :>json int id: The ID of the item.
    :>json string url: The URL of the item's detail view.
    :>json string name: The name of the item.
    :>json object image_content: An object containing the item's image content. May be ``null``.
    :>json object list_content: An object containing the item's list content. May be ``null`.

    :status 200: The profile item's information was succesfully updated.
    :status 404: There is no profile item with the given ``id`` accessible to the requesting user.
