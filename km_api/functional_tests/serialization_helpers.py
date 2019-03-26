"""
Collection of helper functions for reducing repetition when dealing with
serialization in tests.

The main codebase simply uses the actual serializer responsible for the
object type, but we want to maintain a clear separation of the codebase
and these functional tests. Having to change the serialization here
indicates that a potentially breaking change was made.
"""


def user_info(user):
    """
    Get the serialized version of a user's information.

    Args:
        user:
            The user to get the serialized information of.

    Returns:
        A dictionary containing the serialized representation of the
        given user's information.
    """
    return {
        "first_name": user.first_name,
        "image": None,
        "last_name": user.last_name,
    }
