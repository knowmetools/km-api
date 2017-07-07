=======
Know Me
=======

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

    :statuscode 200: The profile's details were retreived succesfully.
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
