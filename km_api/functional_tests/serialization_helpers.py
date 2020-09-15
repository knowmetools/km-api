"""
Collection of helper functions for reducing repetition when dealing with
serialization in functional tests.

The main codebase simply uses the actual serializer responsible for the
object type, but we want to maintain a clear separation of the codebase
and these functional tests. Having to change the serialization here
indicates that a potentially breaking change was made to the output of
an endpoint.
"""
from test_utils import serialized_time


def _has_destroy_perm(_):
    return False


def _is_owner(_):
    return True


def km_user_accessor(
    accessor,
    build_full_url,
    has_destroy_perm=_has_destroy_perm,
    is_owner=_is_owner,
):
    return {
        "id": accessor.pk,
        "url": build_full_url(f"/know-me/accessors/{accessor.pk}/"),
        "created_at": serialized_time(accessor.created_at),
        "updated_at": serialized_time(accessor.updated_at),
        "accept_url": build_full_url(
            f"/know-me/accessors/{accessor.pk}/accept/"
        ),
        "email": accessor.email,
        "is_accepted": accessor.is_accepted,
        "is_admin": accessor.is_admin,
        "km_user": {
            "id": accessor.km_user.pk,
            "image": build_full_file_url(
                accessor.km_user.image, build_full_url
            ),
            "name": accessor.km_user.name,
        },
        "permissions": {
            "accept": has_destroy_perm(accessor),
            "destroy": is_owner(accessor),
            "read": is_owner(accessor),
            "write": is_owner(accessor),
        },
        "user_with_access": user_info(accessor.user_with_access),
    }


def build_full_file_url(file_field, build_full_url):
    """
    Build the full URL for a file field.

    Args:
        file_field:
            The file field to build the full URL for.
        build_full_url:
            The function used to build a full URL out of an absolute
            path.

    Returns:
        The full URL to the file contained in the given field if it
        exists. If the field is empty, ``None`` is returned instead.
    """
    return build_full_url(file_field.url) if file_field else None


def km_user_list(km_users, is_owned_by_user, build_full_url):
    """
    Get the serialized version of a list of Know Me users.

    Args:
        km_users:
            The users to serialize.
        is_owned_by_user:
            A function that returns a boolean indicating if a given user
            is owned by the "current" user.
        build_full_url:
            A function used to take an absolute path and turn it into a
            full URL.

    Returns:
        A list containing the serialized version of each Know Me user.
    """

    def serialize(user):
        return {
            "id": user.pk,
            "url": build_full_url(f"/know-me/users/{user.pk}/"),
            "created_at": serialized_time(user.created_at),
            "updated_at": serialized_time(user.updated_at),
            "is_legacy_user": user.is_legacy_user,
            "is_premium_user": user.is_premium_user,
            "is_owned_by_current_user": is_owned_by_user(user),
            "image": build_full_file_url(user.image, build_full_url),
            "journal_entries_url": build_full_url(
                f"/know-me/users/{user.pk}/journal-entries/"
            ),
            "media_resources_url": build_full_url(
                f"/know-me/users/{user.pk}/media-resources/"
            ),
            "media_resource_cover_styles_url": build_full_url(
                f"/know-me/users/{user.pk}/media-resource-cover-style/"
            ),
            "name": user.name,
            "permissions": {"read": True, "write": is_owned_by_user(user)},
            "profiles_url": build_full_url(
                f"/know-me/users/{user.pk}/profiles/"
            ),
            "quote": user.quote,
            "user_image": build_full_file_url(user.user.image, build_full_url),
        }

    return list(map(serialize, km_users))


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
    if not user:
        return None

    return {
        "first_name": user.first_name,
        "image": None,
        "last_name": user.last_name,
    }
